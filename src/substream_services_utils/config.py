from typing import Optional

_is_local_testing_on = False
_test_user_uuid: Optional[str] = None
_firebase_project_id: Optional[str]


def set_local_testing_on(test_user_uuid: str, firebase_project_id: str):
    global _is_local_testing_on
    global _test_user_uuid
    global _firebase_project_id

    _is_local_testing_on = True
    _test_user_uuid = test_user_uuid
    _firebase_project_id = firebase_project_id


def get_is_local_testing_on():
    return _is_local_testing_on


def get_test_user_uuid():
    return _test_user_uuid


def get_firebase_project_id():
    return _firebase_project_id
