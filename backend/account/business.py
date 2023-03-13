"""
Account business

Business logic for account related operations.
"""
from . import query
from account.models import User, Privacy
from typing import Tuple
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from column.business import create_default_columns
from account.auth_utils import decrypt_token, encrypt_token
from datetime import datetime


def get_or_create_user(payload: dict) -> Tuple[User, bool]:
    is_new = not query.user_exists(payload["sub"])
    user = query.get_or_create_user(payload)
    if is_new:
        create_default_columns(user.id)
        query.create_privacies(user.id)
    return user, encrypt_token(user.google_id, user.last_login)


def update_user(payload: dict) -> None:
    formatted_payload = payload
    try:
        # formats date string from 2023-02-12T16:31:00.000Z to 2023-02-12
        birthday = payload.get("birthday")
        if birthday and len(birthday) < 10:
            raise ValidationError("Invalid Length")
        formatted_payload["birthday"] = birthday[0:10] if birthday else None
        query.update_user(formatted_payload)
    except (IndexError, ValidationError) as err:
        raise AttributeError(err.message + " - " + payload.get("birthday"))


def get_privacies(user_id: int) -> Privacy:
    return query.get_privacies(user_id)


def update_privacies(payload: dict) -> None:
    try:
        privacies = payload.get("privacies")
        uid = payload.get("user_id")
        query.update_privacies(in_user_id=uid, payload=privacies)
    except (AttributeError, IndexError, ValidationError):
        raise AttributeError("Error updating")


def add_friend(user1_id, user2_id):
    if user1_id == user2_id:
        raise ValueError("A user can't befriend themselves")
    else:
        query.add_friend(user1_id, user2_id)


def remove_friend(user1_id, user2_id):
    query.remove_friend(user1_id, user2_id)


def search_users_by_name(search_string) -> list:
    toks = str.split(search_string)
    result = []
    # No mass-searching allowed
    if search_string != "":
        for usr in query.get_all_searchable():
            success = True
            for tok in toks:
                if tok not in usr.first_name and tok not in usr.last_name:
                    success = False
                    break
            if success:
                result.append(usr.to_dict())

    return result


def authenticate_token(token):
    try:
        token_json = decrypt_token(token)
        user = query.get_user_by_token_fields(
            token_json["google_id"],
            datetime.strptime(token_json["last_login"], "%Y-%m-%d %H:%M:%S.%f%z"),
        )
        return user, encrypt_token(user.google_id, user.last_login)
    except ObjectDoesNotExist as err:
        raise ObjectDoesNotExist("Failed to Authenticate Token") from err
