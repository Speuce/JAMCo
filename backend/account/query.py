"""
Account queries

Query functions for account related operations.
"""

from django.core.exceptions import ObjectDoesNotExist
from .models import User
import datetime

def get_or_create_user(payload:dict) -> int:
    try:
        return User.objects.get(google_id=payload['google_id']).id
    except ObjectDoesNotExist:
        # TODO: Replace these dummy values with values populated using OAuth (#26)
        return User.objects.create(
            google_id=payload['google_id'],
            image_url='https://i.redd.it/9m2wxxxoljk91.jpg',
            country='The Canada',
            city='Middle of nowhere',
            birthday=datetime.date(1970, 1, 1),
            field_of_work="Wouldn't you like to know",
        ).id
