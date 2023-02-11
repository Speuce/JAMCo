"""
Account queries

Query functions for account related operations.
"""

import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import datetime

def get_or_create_user(payload: dict) -> User:
    try:
        return User.objects.get(google_id=payload['google_id'])
    except ObjectDoesNotExist:
        # TODO: Replace these dummy values with values populated using OAuth (#26)
        return User.objects.create(
            username=User.objects.all().count(),
            google_id=payload['google_id'],
            image_url='https://i.redd.it/9m2wxxxoljk91.jpg',
            country='The Canada',
            city='Middle of nowhere',
            birthday=datetime.date(1970, 1, 1),
            field_of_work="Wouldn't you like to know",
        )


def user_exists(credential: str) -> bool:
    return User.objects.filter(google_id=credential).exists()


def update_user(payload: dict):
    user = User.objects.get(google_id=payload['google_id'])
    for key, value in payload.items():
        # If there are invalid keys in the payload (e.g. the frontend misspelled
        # the name of a field), raise an exception
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            raise AttributeError('User has no attribute ' + key)

    # Since this is at the end of the loop, it'll only execute if an exception
    # isn't raised. That is, we'll only save changes if the entire payload is
    # error-free.
    user.save()


def create_column(credential: str, column_name: str) -> KanbanColumn:
    return KanbanColumn.objects.create(
        user=User.objects.get(google_id=credential),
        name=column_name,
        column_number=KanbanColumn.objects.all().count()
    )


def get_columns(credential: str) -> list[KanbanColumn]:
    return KanbanColumn.objects.filter(
        user=User.objects.get(google_id=credential))


def rename_column(
        credential: str, column_number: int, new_name: str) -> KanbanColumn:
    column = KanbanColumn.objects.get(
        user=User.objects.get(google_id=credential),
        column_number=column_number
    )
    column.name = new_name
    column.save()
    return column


def delete_column(credential: str, column_number: int):
    KanbanColumn.objects.get(
        user=User.objects.get(google_id=credential),
        column_number=column_number
    ).delete()

