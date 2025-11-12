from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from substream_services_utils.config import get_is_local_testing_on, get_test_user_uuid

_auth_scheme = HTTPBearer()


def get_firebase_user(
        credentials: HTTPAuthorizationCredentials = Depends(_auth_scheme)
) -> str:
    if get_is_local_testing_on():
        return get_test_user_uuid()

    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        token = credentials.credentials
        user_data = auth.verify_id_token(token, check_revoked=True)

        return user_data['uid']
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def ban_user(user_uid: str):
    auth.update_user(
        user_uid,
        disabled=True
    )
