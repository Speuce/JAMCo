"""
Account queries

Query functions for account related operations.
"""

from account.models import User
from column.models import KanbanColumn


def create_column(user_id: int, column_name: str, column_number: int) -> KanbanColumn:
    return KanbanColumn.objects.create(user=User.objects.get(id=user_id), name=column_name, column_number=column_number)


def get_columns(user_id: int) -> list[KanbanColumn]:
    return KanbanColumn.objects.filter(user=User.objects.get(id=user_id))


def delete_column(user_id: int, column_number: int):
    KanbanColumn.objects.get(user=user_id, column_number=column_number).delete()


def delete_columns(ids: list[int]):
    for column_id in ids:
        KanbanColumn.objects.filter(id=column_id).delete()
