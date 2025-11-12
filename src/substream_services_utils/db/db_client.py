from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore
from google.auth.credentials import AnonymousCredentials
from google.cloud.firestore_v1 import Client

FIREBASE_EMULATOR_PROJECT_ID = "firebase-emulator"


def init_firebase(
        firebase_service_account_key_path: str,
        using_firebase_emulator=False,
):
    if using_firebase_emulator:
        cred = AnonymousCredentials()
        options = {"projectId": FIREBASE_EMULATOR_PROJECT_ID}
    else:
        cred = credentials.Certificate(firebase_service_account_key_path)
        options = {}

    firebase_admin.initialize_app(cred, options=options)


@lru_cache(maxsize=1)
def get_db_client() -> Client:
    return firestore.client()
