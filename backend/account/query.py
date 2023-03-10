"""
Account queries

Query functions for account related operations.
"""

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from account.models import User, Privacy, FriendRequest
from django.db.models.query import QuerySet


def get_or_create_user(payload: dict) -> User:
    try:
        user = User.objects.get(google_id=payload["sub"])
        update_user_last_login(user)
        return user
    except ObjectDoesNotExist:
        return User.objects.create(
            username=User.objects.all().count(),
            google_id=payload["sub"],
            email=payload["email"] if payload.get("email") else "",
            image_url=payload["picture"] if payload.get("picture") else "https://i.imgur.com/QJpNyuN.png",
            first_name=payload["given_name"] if payload.get("given_name") else "",
            last_name=payload.get("family_name") if payload.get("family_name") else "",
            last_login=timezone.now(),
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


def create_privacies(in_user_id):
    Privacy.objects.create(
        user=User.objects.get(id=in_user_id),
        is_searchable=True,
        share_kanban=True,
        cover_letter_requestable=True,
    )


def get_privacies(in_user_id) -> Privacy:
    return Privacy.objects.get(user__id=in_user_id)


def update_privacies(in_user_id, payload: dict):
    privacies = Privacy.objects.get(user__id=in_user_id)
    for key, value in payload.items():
        # If there are invalid keys in the payload, raise an exception
        if hasattr(privacies, key):
            setattr(privacies, key, value)
        else:
            raise AttributeError("Privacy has no attribute " + key)

    # Will only execute if an exception isn't raised
    privacies.save()


def add_friend(user1_id, user2_id):
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    user1.friends.add(user2)


def remove_friend(user1_id, user2_id):
    user1 = User.objects.get(id=user1_id)
    user2 = User.objects.get(id=user2_id)

    user1.friends.remove(user2)


def get_user_by_token_fields(google_id, last_login) -> User:
    user = User.objects.get(google_id=google_id, last_login=last_login)
    update_user_last_login(user)
    return user


def update_user_last_login(user) -> None:
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])


def create_friend_request(from_user_id, to_user_id) -> FriendRequest:
    return FriendRequest.objects.create(
        from_user=User.objects.get(id=from_user_id),
        to_user=User.objects.get(id=to_user_id),
        sent=timezone.now(),
        accepted=False,
        acknowledged=None,
    )


def accept_friend_request(request_id, to_user_id) -> None:
    request = FriendRequest.objects.get(id=request_id, to_user_id=to_user_id)

    to_user = request.to_user
    from_user = request.from_user

    from_user.friends.add(to_user)
    to_user.friends.add(from_user)

    to_user.save()
    from_user.save()

    request.accepted = True
    request.acknowledged = timezone.now()
    request.save()


def deny_friend_request(request_id, to_user_id) -> None:
    request = FriendRequest.objects.get(id=request_id, to_user__id=to_user_id)

    request.acknowledged = timezone.now()
    request.save()


def get_friend_requests_status(user_id) -> list[QuerySet, QuerySet]:
    sent = FriendRequest.objects.filter(from_user__id=user_id)
    received = FriendRequest.objects.filter(to_user__id=user_id)

    return sent, received


def pending_friend_request_exists(request_id=None, from_user_id=None, to_user_id=None) -> bool:
    if request_id:
        if not to_user_id:
            raise ValidationError("to_user_id must be passed when request_id passed")
        return FriendRequest.objects.filter(id=request_id, to_user__id=to_user_id, acknowledged=None).exists()
    if not to_user_id or not from_user_id:
        raise ValidationError("both to_user_id and from_user_id must be passed when request_id not passed")
    return (
        FriendRequest.objects.filter(from_user__id=from_user_id, to_user__id=to_user_id, acknowledged=None).exists()
        or FriendRequest.objects.filter(from_user__id=to_user_id, to_user__id=from_user_id, acknowledged=None).exists()
    )


def are_friends(user_id_one, user_id_two) -> bool:
    user_one = User.objects.get(id=user_id_one)
    user_two = User.objects.get(id=user_id_two)
    return user_one.friends.contains(user_two)
