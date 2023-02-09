"""
Account queries

Query functions for account related operations.
"""

import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import User

def get_or_create_user(payload: dict) -> User:
    try:
        return User.objects.get(google_id=payload['google_id'])
    except ObjectDoesNotExist:
        # TODO: Replace these dummy values with values populated using OAuth (#26)
        return User.objects.create(
            google_id=payload['google_id'],
            image_url='https://i.redd.it/9m2wxxxoljk91.jpg',
            country='The Canada',
            city='Middle of nowhere',
            birthday=datetime.date(1970, 1, 1),
            field_of_work="Wouldn't you like to know",
        )


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
