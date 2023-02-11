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


def get_columns(credential: str) -> list[KanbanColumn]:
    columns = query.get_columns(credential)
    # Make sure the columns are sorted
    return columns.order_by('column_number')


def rename_column(
        credential: str, column_number: int, new_name: str) -> KanbanColumn:
    return query.rename_column(credential, column_number, new_name)


def reorder_column(
        credential: str,
        column_number: int,
        new_column_number: str
    ) -> KanbanColumn:

    changed_columns = []

    columns = list(get_columns(credential))

    if not 0 <= column_number < len(columns):
        raise ValueError(f"Source column number ({column_number}) must be \
                         between 0 and the number of the user's columns \
                         ({len(columns)})"
                        )
    if not 0 <= new_column_number < len(columns):
        raise ValueError(f"New column number ({new_column_number}) must be \
                         between 0 and the number of the user's columns \
                         ({len(columns)})"
                        )

    if column_number < new_column_number:
        # create_column and this function ensure that the index of each column
        # in this list is equal to that column's number (at least until we start
        # modifying it)
        for i in range(column_number + 1, new_column_number + 1):
            columns[i].column_number -= 1
            changed_columns.append(columns[i])
        columns[column_number].column_number = new_column_number
        changed_columns.append(columns[column_number])

    elif new_column_number < column_number:
        columns[column_number].column_number = new_column_number
        changed_columns.append(columns[column_number])
        for i in range(new_column_number, column_number):
            columns[i].column_number += 1
            changed_columns.append(columns[i])

    for column in changed_columns:
        column.save()

    return changed_columns
