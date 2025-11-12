from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

_is_local_testing_on = False
_test_user_uuid: Optional[str] = None

_auth_scheme = HTTPBearer()


def set_local_testing_on(test_user_uuid: str):
    global _is_local_testing_on
    global _test_user_uuid

    _is_local_testing_on = True
    _test_user_uuid = test_user_uuid


def get_firebase_user(
        credentials: HTTPAuthorizationCredentials = Depends(_auth_scheme)
) -> str:
    if _is_local_testing_on:
        return _test_user_uuid

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
