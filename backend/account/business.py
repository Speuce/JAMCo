"""
Account business

Business logic for account related operations.
"""
from . import query
from account.models import User, Privacy
from typing import Tuple
from django.core.exceptions import ValidationError
from column.business import create_default_columns


def get_or_create_user(payload: dict) -> Tuple[User, bool]:
    is_new = not query.user_exists(payload["sub"])
    user = query.get_or_create_user(payload)
    if is_new:
        create_default_columns(user.id)
        query.create_privacies(user.id)

    return user, is_new


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
        query.update_privacies(user_id=uid, payload=privacies)
    except (AttributeError, IndexError, ValidationError):
        raise AttributeError("Error updating")


def add_friend(user1_id, user2_id):
    if user1_id == user2_id:
        raise ValueError("A user can't befriend themselves")
    else:
        query.add_friend(user1_id, user2_id)


def remove_friend(user1_id, user2_id):
    query.remove_friend(user1_id, user2_id)
