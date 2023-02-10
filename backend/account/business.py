"""
Account business

Business logic for account related operations.
"""

from . import query
from .models import *

def get_or_create_user(payload: dict) -> User:
    return query.get_or_create_user(payload)


def update_user(payload: dict):
    query.update_user(payload)


def create_column(credential: str, column_name: str) -> KanbanColumn:
    return query.create_column(credential, column_name)