"""
Account business

Business logic for account related operations.
"""

from . import query
from .models import *

def get_or_create_user(payload: dict) -> User:
    is_new = not query.user_exists(payload['google_id'])
    user = query.get_or_create_user(payload)
    if (is_new):
        create_default_columns(payload['google_id'])

    return user


def update_user(payload: dict):
    query.update_user(payload)


def create_column(
        credential: str, column_name: str, column_number: int) -> KanbanColumn:
    # Create the new column and then put in in its proper place
    new_column = query.create_column(credential, column_name)
    reorder_column(credential, new_column.column_number, column_number)

    return new_column


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


def delete_column(credential: str, column_number: int) -> list[KanbanColumn]:
    changed_columns = []

    columns = list(get_columns(credential))

    if not 0 <= column_number < len(columns):
        raise ValueError(f"Column number to delete ({column_number}) must be \
                         between 0 and the number of the user's columns \
                         ({len(columns)})"
                        )

    for i in range(column_number + 1, len(columns)):
        columns[i].column_number -= 1
        changed_columns.append(columns[i])

    query.delete_column(credential, column_number)

    for column in changed_columns:
        column.save()

    return changed_columns


def create_default_columns(credential: str):
    create_column(credential, 'To Apply', 0)
    create_column(credential, 'Application Submitted', 1)
    create_column(credential, 'OA', 2)
    create_column(credential, 'Interview', 3)


def update_columns(credential: str, payload: list[dict]) -> list[KanbanColumn]:
    # Ensure that all fields are present and valid before doing any operations
    for column_spec in payload:
        if 'id' not in column_spec:
            raise ValueError(f'Column {column_spec} missing field: id')
        if 'name' not in column_spec:
            raise ValueError(f'Column {column_spec} missing field: name')
        if 'column_number' not in column_spec:
            raise ValueError(f'Column {column_spec} missing field: \
                             column_number')

    # TODO: Go through the columns in the db and delete those whose ids in don't appear in the payload
    existing_columns = {column.id: column for column in get_columns(credential)}

    for column_spec in payload:
        column_id = column_spec['id']
        if column_id not in existing_columns:
            # Create a new column
            create_column(
                credential, column_spec['name'], column_spec['column_number'])
        elif column_spec['name'] != existing_columns[column_id].name:
            # Rename
            existing_columns[column_id].name = column_spec['name']

            # TODO: Reorder

    for column in existing_columns.values():
        column.save()

    return get_columns(credential)
