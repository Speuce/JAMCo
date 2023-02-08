"""
Account business

Business logic for account related operations.
"""

from . import query

def get_or_create_user(payload: dict) -> int:
    return query.get_or_create_user(payload)
