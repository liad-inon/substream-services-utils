from google.cloud.firestore_v1 import DocumentReference
from pydantic import ValidationError


class DbException(Exception):
    pass

class NoneExistentResource(Exception):
    pass

class NoneExistentDocumentError(NoneExistentResource):
    def __init__(self, document_ref: DocumentReference):
        self.document_ref = document_ref
        super().__init__(
            f"Document with path '{document_ref.path}' does not exist."
        )


class NoneExistentFieldError(NoneExistentResource):
    def __init__(self, document_ref: DocumentReference, field_key: str):
        self.document_ref = document_ref
        super().__init__(
            f"'{field_key}' field key not exists '{document_ref.path}' document."
        )


class SchemaTypeError(TypeError):
    def __init__(self, expected_schema, actual_instance):
        self.expected_schema = expected_schema
        self.actual_instance = actual_instance
        super().__init__(
            f"Expected an instance of {expected_schema.__name__}, "
            f"but got {type(actual_instance).__name__}."
        )


class InvalidDocumentSchema(DbException):
    def __init__(self, document_ref: DocumentReference, validation_error: ValidationError):
        self.document_ref = document_ref
        self.validation_error = validation_error
        super().__init__(
            f"The document at '{document_ref.path}' is not "
            f"compatible with the given schema: {validation_error}"
        )
