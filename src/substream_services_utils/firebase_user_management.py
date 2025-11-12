from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, _auth_utils
from firebase_admin.auth import UserRecord
from firebase_admin.exceptions import FirebaseError

from substream_services_utils.config import get_is_local_testing_on, get_test_user_uuid

FIREBASE_WEAK_PASSWORD_ERROR_CODE = "WEAK_PASSWORD"
FIREBASE_INVALID_EMAIL_ERROR_CODE = "INVALID_EMAIL"

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


def create_new_user_with_email_and_password(
        email: str,
        password: str,
) -> UserRecord:
    # This is an extremely unideal solution. The create user function
    # Will return a value error if the email or password are invalid,
    # and the only way to detect is checking the error string which is
    # even less reliable than calling the private validation functions
    # them self. There is a possibility to make the firebase requests directly
    # but this means to implement the authentication to firebase admin my self.
    try:
        _auth_utils.validate_password(password)
    except ValueError:
        raise FirebaseError(
            code=FIREBASE_WEAK_PASSWORD_ERROR_CODE,
            message=f"password '{password}' is to weak"
        )

    try:
        _auth_utils.validate_email(email)
    except ValueError:
        raise FirebaseError(
            code=FIREBASE_INVALID_EMAIL_ERROR_CODE,
            message=f"email '{password}' is invalid"
        )

    return auth.create_user(
        email=email,
        password=password,
    )


def ban_user(user_uid: str):
    auth.update_user(
        user_uid,
        disabled=True
    )
