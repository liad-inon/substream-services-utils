# --- Core Public API ---
from .core import (
    DataBaseAccess,
    init_firebase,
    get_db_client
)

# --- Custom Exceptions ---
from .exceptions import (
    DbException,
    InvalidDocumentSchema,
    NoneExistentDocumentError,
    NoneExistentFieldError,
    NoneExistentResource,
    SchemaTypeError,
)

# --- Firestore Abstractions ---
from .firestore_wrappers import (
    DocumentType,
    FieldType,
    FirestoreCollection,
    FirestoreDocument,
    FirestoreField,
)

# --- Schema Definitions and Schema Constants ---
from .schemas import (
    STATUS_MESSAGE_FIELD,
    SUBSCRIPTION_TYPE_FIELD,
    TRANSCRIPTION_JOB_PROGRESS_COLLECTION,
    TRANSCRIPTION_MINUTES_LEFT_FIELD,
    USER_DATA_COLLECTION,
    USER_NAME_FIELD,
    TranscriptionJobProgress,
    UserData,
)


__all__ = [
    # Core API
    'DataBaseAccess',
    'init_firebase',
    'get_db_client',

    # Exceptions
    'DbException',
    'InvalidDocumentSchema',
    'NoneExistentDocumentError',
    'NoneExistentFieldError',
    'NoneExistentResource',
    'SchemaTypeError',

    # Firestore Abstractions
    'DocumentType',
    'FieldType',
    'FirestoreCollection',
    'FirestoreDocument',
    'FirestoreField',

    # Schemas and Schema Constants
    'STATUS_MESSAGE_FIELD',
    'SUBSCRIPTION_TYPE_FIELD',
    'TRANSCRIPTION_JOB_PROGRESS_COLLECTION',
    'TRANSCRIPTION_MINUTES_LEFT_FIELD',
    'USER_DATA_COLLECTION',
    'USER_NAME_FIELD',
    'TranscriptionJobProgress',
    'UserData',
]