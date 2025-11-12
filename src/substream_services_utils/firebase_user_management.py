from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from app.config import Settings
from app.global_consts import ENV_LOCAL_TEST

_auth_scheme = HTTPBearer()


def get_firebase_user(
        credentials: HTTPAuthorizationCredentials = Depends(_auth_scheme)
) -> str:
    app_settings = Settings.get()

    if app_settings.ENVIRONMENT == ENV_LOCAL_TEST:
        return app_settings.TEST_USER_UID

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
