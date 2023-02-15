"""
Account business

Business logic for account related operations.
"""
from . import query
from .models import *
from typing import Tuple
from django.core.exceptions import ValidationError


def get_or_create_user(payload: dict) -> Tuple[User, bool]:
    is_new = not query.user_exists(payload["sub"])
    user = query.get_or_create_user(payload)
    if is_new:
        create_default_columns(user.id)

    return user, is_new


def update_user(payload: dict) -> None:
    formatted_payload = payload
    try:
        # formats date string from 2023-02-12T16:31:00.000Z to 2023-02-12
        formatted_payload['birthday'] = payload.get('birthday')[0:10] if payload.get('birthday') else None
        query.update_user(formatted_payload)
    except (IndexError, ValidationError):
        raise AttributeError("Failed to format date: " + payload.get('birthday'))
    


def get_columns(user_id: int) -> list[KanbanColumn]:
    columns = query.get_columns(user_id)
    # Make sure the columns are sorted
    return list(columns.order_by("column_number"))


def create_default_columns(user_id: int):
    query.create_column(user_id, "To Apply", 0)
    query.create_column(user_id, "Application Submitted", 1)
    query.create_column(user_id, "OA", 2)
    query.create_column(user_id, "Interview", 3)


def update_columns(user_id: int, payload: list[dict]) -> list[KanbanColumn]:
    # Ensure that all fields are present and valid before doing any operations
    for column_spec in payload:
        if "id" not in column_spec:
            raise ValueError(f"Column {column_spec} missing field: id")
        if "name" not in column_spec:
            raise ValueError(f"Column {column_spec} missing field: name")
        if "column_number" not in column_spec:
            raise ValueError(
                f"Column {column_spec} missing field: \
                             column_number"
            )

    # Separate current columns into ones to update and ones to delete
    ids_in_payload = [column_spec["id"] for column_spec in payload]
    existing_columns = {}
    ids_to_delete = []
    for column in get_columns(user_id):
        if column.id in ids_in_payload:
            existing_columns[column.id] = column
        else:
            ids_to_delete.append(column.id)
    # Delete columns whose ids aren't in the payload
    query.delete_columns(ids_to_delete)

    # Create, rename, and reorder columns
    for column_spec in payload:
        column_id = column_spec["id"]
        if column_id not in existing_columns:
            # Create a new column
            query.create_column(
                user_id, column_spec["name"], column_spec["column_number"]
            )
        else:
            # Rename
            existing_columns[column_id].name = column_spec["name"]
            # Reorder
            existing_columns[column_id].column_number = column_spec["column_number"]

    for column in existing_columns.values():
        column.save()

    return get_columns(user_id)
