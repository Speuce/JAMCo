"""
Account queries

Query functions for account related operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from account.models import User


def get_or_create_user(payload: dict) -> User:
    try:
        return User.objects.get(google_id=payload["sub"])
    except ObjectDoesNotExist:
        return User.objects.create(
            username=User.objects.all().count(),
            google_id=payload["sub"],
            email=payload["email"] if payload.get("email") else "No Email Found",
            image_url=payload["picture"] if payload.get("picture") else None,
            first_name=payload["given_name"] if payload.get("given_name") else "No First Name Found",
            last_name=payload.get("family_name") if payload.get("family_name") else "",
        )


def user_exists(google_id: str) -> bool:
    return User.objects.filter(google_id=google_id).exists()


def update_user(payload: dict):
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


def add_friend(user1_id, user2_id):
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    user1.friends.add(user2)


def remove_friend(user1_id, user2_id):
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    user1.friends.remove(user2)
