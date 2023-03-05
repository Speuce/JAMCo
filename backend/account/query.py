"""
Account queries

Query functions for account related operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from account.models import User, Privacy


def get_or_create_user(payload: dict) -> User:
    try:
        return User.objects.get(google_id=payload["sub"])
    except ObjectDoesNotExist:
        return User.objects.create(
            username=User.objects.all().count(),
            google_id=payload["sub"],
            email=payload["email"] if payload.get("email") else "",
            image_url=payload["picture"] if payload.get("picture") else "https://i.imgur.com/QJpNyuN.png",
            first_name=payload["given_name"] if payload.get("given_name") else "",
            last_name=payload.get("family_name") if payload.get("family_name") else "",
        )


def user_exists(google_id: str) -> bool:
    return User.objects.filter(google_id=google_id).exists()


def update_user(payload: dict):
    # updates based on user_id rather than google_id
    user = User.objects.get(id=payload.get("id"))
    for key, value in payload.items():
        # If there are invalid keys in the payload (e.g. the frontend misspelled
        # the name of a field), raise an exception
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            raise AttributeError("User has no attribute " + key)

    # Since this is at the end of the func, it'll only execute if an exception
    # isn't raised. That is, we'll only save changes if the entire payload is
    # error-free.
    user.save()


def create_privacies(user_id) -> Privacy:
    # potential option for defaults? i.e. all True vs all False
    return Privacy.objects.create(
        user=User.objects.get(id=user_id),
        is_searchable=True,
        share_kanban=True,
        cover_letter_requestable=True,
    )


def get_privacies(user_id) -> Privacy:
    return Privacy.objects.get(user__id=user_id)


def update_privacies(user_id, payload: dict):
    privacies = Privacy.objects.get(user__id=user_id)
    for key, value in payload.items():
        # If there are invalid keys in the payload (e.g. the frontend misspelled
        # the name of a field), raise an exception
        if hasattr(privacies, key):
            setattr(privacies, key, value)
        else:
            raise AttributeError("Privacy has no attribute " + key)

    # Since this is at the end of the func, it'll only execute if an exception
    # isn't raised. That is, we'll only save changes if the entire payload is
    # error-free.
    privacies.save()


def add_friend(user1_id, user2_id):
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    user1.friends.add(user2)


def remove_friend(user1_id, user2_id):
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    user1.friends.remove(user2)
