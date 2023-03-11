"""
Account business

Business logic for account related operations.
"""
from . import query
from account.models import User, Privacy, FriendRequest
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
    if not query.are_friends(user1_id, user2_id):
        raise ObjectDoesNotExist("Error Removing Friends")
    query.remove_friend(user1_id, user2_id)


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


def create_friend_request(from_user_id, to_user_id) -> FriendRequest:
    try:
        pending_request_exists = query.pending_friend_request_exists(from_user_id=from_user_id, to_user_id=to_user_id)
        already_friends = query.are_friends(user_id_one=from_user_id, user_id_two=to_user_id)
        user_not_searchable = not query.get_privacies(to_user_id).is_searchable

        if pending_request_exists or already_friends or user_not_searchable:
            raise ValueError("Unable to Create Friend Request")

        return query.create_friend_request(from_user_id, to_user_id)
    except ObjectDoesNotExist as err:
        raise ObjectDoesNotExist("Error Creating Friend Request") from err


def accept_friend_request(request_id, to_user_id, from_user_id) -> None:
    if query.pending_friend_request_exists(request_id=request_id, to_user_id=to_user_id, from_user_id=from_user_id):
        try:
            add_friend(to_user_id, from_user_id)
            query.accept_friend_request(request_id=request_id, to_user_id=to_user_id, from_user_id=from_user_id)
        except ValueError as err:
            raise err
    else:
        raise ObjectDoesNotExist("Friend Request Does Not Exist")


def deny_friend_request(request_id, to_user_id, from_user_id) -> None:
    if query.pending_friend_request_exists(request_id=request_id, to_user_id=to_user_id, from_user_id=from_user_id):
        query.deny_friend_request(request_id=request_id, to_user_id=to_user_id, from_user_id=from_user_id)
    else:
        raise ObjectDoesNotExist("Friend Request Does Not Exist")


def get_friend_requests_status(user_id) -> list[FriendRequest, FriendRequest]:
    return query.get_friend_requests_status(user_id)
