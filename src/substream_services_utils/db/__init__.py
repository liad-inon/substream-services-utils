from google.cloud.firestore_v1 import Client

from firestore_wrappers import FirestoreCollection
from schemas import UserData, TranscriptionJobProgress

# --- COLLECTION KEYS ---
USER_DATA_COLLECTION = "userData"
TRANSCRIPTION_JOB_PROGRESS_COLLECTION = "subtitlesCreationJobProgres"

# --- userData FIELDS ---
TRANSCRIPTION_MINUTES_LEFT_FIELD = "transcriptionMinutesLeft"
USER_NAME_FIELD = "userName"
SUBSCRIPTION_TYPE_FIELD = "subscriptionType"

# --- subtitlesCreationStatus FIELDS ---
STATUS_MESSAGE_FIELD = "statusMessage"


class DataBaseAccess:
    def __init__(self, db_client: Client):
        self.user_data = FirestoreCollection(
            db_client,
            USER_DATA_COLLECTION,
            UserData
        )
        self.transcription_job_progress = FirestoreCollection(
            db_client,
            TRANSCRIPTION_JOB_PROGRESS_COLLECTION,
            TranscriptionJobProgress
        )
