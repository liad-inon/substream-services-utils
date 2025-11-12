from __future__ import annotations

from typing import TypeVar, Generic, Type, Callable, Any

from google.api_core.exceptions import AlreadyExists
from google.cloud.exceptions import NotFound
from google.cloud.firestore_v1 import DocumentReference, transactional, Client, Transaction
from pydantic import BaseModel, ValidationError

from app.db.exceptions import NoneExistentFieldError, InvalidDocumentSchema, SchemaTypeError, NoneExistentDocumentError

DocumentType = TypeVar('DocumentType', bound=BaseModel)
FieldType = TypeVar('FieldType')


class FirestoreField(Generic[FieldType]):
    def __init__(
            self,
            field_key: str,
            document_wrapper: FirestoreDocument[Any],
            field_type: Type[FieldType],
    ):
        self._field_key = field_key
        self._document_wrapper = document_wrapper
        self._field_type = field_type

    def get(self) -> FieldType:
        document_data = self._document_wrapper.get()

        self._validate_field_exist_in(document_data)

        return getattr(document_data, self._field_key)

    def set(self, new_value: FieldType):
        if not isinstance(new_value, self._field_type):
            raise ValueError(f"new_value type is incorrect. expected '{self._field_type}', got '{type(new_value)}'")

        try:
            self._document_wrapper.document_ref.update(
                {self._field_key: new_value}
            )
        except NotFound:
            raise NoneExistentDocumentError(self._document_wrapper.document_ref)

    def transactional_set(self, change_field_callback: Callable[[FieldType], FieldType]):
        def _transform_document_callback(document_data: DocumentType):
            self._validate_field_exist_in(document_data)

            curr_field_value = getattr(document_data, self._field_key)
            new_field_value = change_field_callback(curr_field_value)
            setattr(document_data, self._field_key, new_field_value)

            return document_data

        self._document_wrapper.transactional_set(
            _transform_document_callback
        )

    def _validate_field_exist_in(self, document_data: DocumentType):
        if self._field_key not in document_data.model_fields.keys():
            raise NoneExistentFieldError(self._document_wrapper.document_ref, self._field_key)

    @property
    def field_key(self):
        return self._field_key

    @property
    def field_type(self):
        return self._field_type


class FirestoreDocument(Generic[DocumentType]):
    def __init__(self, db_client: Client, document_ref: DocumentReference, schema: Type[DocumentType]):
        self._db_client = db_client
        self._document_ref = document_ref
        self._schema = schema

    def get(self) -> DocumentType:
        document_dict = self._document_ref.get().to_dict()

        if not document_dict:
            raise NoneExistentDocumentError(self._document_ref)

        try:
            return self._schema.model_validate(document_dict)
        except ValidationError as exception:
            raise InvalidDocumentSchema(self._document_ref, exception)

    def set(self, new_data: DocumentType):
        if not isinstance(new_data, self._schema):
            raise SchemaTypeError(self._schema, new_data)

        self._document_ref.set(new_data.model_dump())

    def update_fields(self, new_values_map: dict):
        for field_key, field_value in new_values_map.items():
            self.filed(field_key).set(field_value)

    def filed(self, field_name: str):
        document_fields = self._schema.model_fields

        if field_name not in document_fields.keys():
            raise ValueError(f"{field_name} is not an existing document field")

        field_type = document_fields[field_name].annotation

        return FirestoreField(field_name, self, field_type)

    def transactional_set(self, data_transform_callback: Callable[[DocumentType], DocumentType]):
        @transactional
        def _transaction_callback(transaction: Transaction):
            snapshot = self._document_ref.get(transaction=transaction)

            if not snapshot.exists:
                raise NoneExistentDocumentError(self._document_ref)

            current_data = self._schema.model_validate(snapshot.to_dict())
            new_data = data_transform_callback(current_data)

            if not isinstance(new_data, self._schema):
                raise SchemaTypeError(self._schema, new_data)

            transaction.set(self._document_ref, new_data.model_dump())

        transaction = self._db_client.transaction()
        _transaction_callback(transaction)

    def delete(self):
        self._document_ref.delete()

    @property
    def document_ref(self):
        return self._document_ref

    @property
    def schema(self):
        return self._schema


class FirestoreCollection(Generic[DocumentType]):
    def __init__(self, db_client: Client, collection_key: str, documents_schema: Type[DocumentType]):
        self._db_client = db_client
        self._collection_ref = db_client.collection(collection_key)
        self._documents_schema = documents_schema

    def document(self, document_key):
        document_ref = self._collection_ref.document(document_key)

        return FirestoreDocument(self._db_client, document_ref, self._documents_schema)

    def create_document(self, document_key: str, data: DocumentType) -> FirestoreDocument[DocumentType]:
        if not isinstance(data, self._documents_schema):
            raise TypeError("Data does not match the document schema for this collection.")

        document_ref = self._collection_ref.document(document_key)

        try:
            document_ref.create(data.model_dump())
        except AlreadyExists:
            raise ValueError(f"Document with key '{document_key}' already exists in the collection.")

        return FirestoreDocument(self._db_client, document_ref, self._documents_schema)

    @property
    def collection_ref(self):
        return self._collection_ref

    @property
    def documents_schema(self):
        return self._documents_schema
