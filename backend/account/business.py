"""
Account business

Business logic for account related operations.
"""

from . import query
from .models import User

def get_or_create_user(payload: dict) -> User:
    return query.get_or_create_user(payload)


def update_user(payload: dict):
    query.update_user(payload)