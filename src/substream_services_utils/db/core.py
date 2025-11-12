from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore_v1 import Client

from .firestore_wrappers import FirestoreCollection
from .schemas import UserData, TranscriptionJobProgress, USER_DATA_COLLECTION, TRANSCRIPTION_JOB_PROGRESS_COLLECTION


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


def init_firebase(
        firebase_service_account_key_path: str,
        using_firebase_emulator=False,
        firebase_emulator_project_id: str=None
):
    if using_firebase_emulator:
        if not firebase_emulator_project_id:
            raise ValueError("firebase_emulator_project_id argument is None.")

        cred = AnonymousCredentials()
        options = {"projectId": firebase_emulator_project_id}
    else:
        cred = credentials.Certificate(firebase_service_account_key_path)
        options = {}

    firebase_admin.initialize_app(cred, options=options)


@lru_cache(maxsize=1)
def get_db_client() -> Client:
    return firestore.client()
