"""
Account business

Business logic for account related operations.
"""
from . import query
from account.models import User
from typing import Tuple
from django.core.exceptions import ValidationError
from column.business import create_default_columns


def get_or_create_user(payload: dict) -> Tuple[User, bool]:
    is_new = not query.user_exists(payload["sub"])
    user = query.get_or_create_user(payload)
    if is_new:
        create_default_columns(user.id)

    return user, is_new


def update_user(payload: dict) -> None:
    formatted_payload = payload
    try:
        # formats date string from 2023-02-12T16:31:00.000Z to 2023-02-12
        formatted_payload["birthday"] = payload.get("birthday")[0:10] if payload.get("birthday") else None
        query.update_user(formatted_payload)
    except (IndexError, ValidationError):
        raise AttributeError("Failed to format date: " + payload.get("birthday"))
