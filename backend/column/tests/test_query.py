from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from column import query
from account.tests.factories import UserFactory
from column.tests.factories import KanbanColumnFactory


class CreateColumnTests(TestCase):
    def test_create_column(self):
        user = UserFactory()

        new_column = query.create_column(user.id, "New column", 0)
        newer_column = query.create_column(user.id, "Newer column", 1)

        # Column numbers should be in order of creation by default
        self.assertEqual(new_column.column_number, 0)
        self.assertEqual(newer_column.column_number, 1)

    def test_duplicate_column_names(self):
        user = UserFactory()
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newer column", 1)

        # Duplicate names are allowed
        duplicate_name_column = query.create_column(user.id, "Newer column", 2)
        self.assertEqual(duplicate_name_column.column_number, 2)

    def test_invalid_create_column(self):
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.create_column(-1, "New column", 0)


class GetColumnsTests(TestCase):
    def test_get_columns(self):
        user = UserFactory()
        KanbanColumnFactory(user=user)
        KanbanColumnFactory(user=user)
        KanbanColumnFactory(user=user)
        # Make another user
        user2 = UserFactory()
        KanbanColumnFactory(user=user2)
        KanbanColumnFactory(user=user2)
        KanbanColumnFactory(user=user2)
        KanbanColumnFactory(user=user2)

        columns = query.get_columns(user.id)

        # The query should only return the columns for the specified user
        self.assertEqual(columns.count(), 3)
        for column in columns:
            self.assertEqual(column.user.id, user.id)


class DeleteColumnsTests(TestCase):
    def test_delete_columns(self):
        user = UserFactory()
        column1 = KanbanColumnFactory(user=user, column_number=1)
        column2 = KanbanColumnFactory(user=user, column_number=2)
        KanbanColumnFactory(user=user, column_number=3)
        # Make another user
        user2 = UserFactory()
        KanbanColumnFactory(user=user2)
        KanbanColumnFactory(user=user2)
        KanbanColumnFactory(user=user2)
        KanbanColumnFactory(user=user2)

        query.delete_columns([column1.id, column2.id])
        self.assertEqual(len(query.get_columns(user.id)), 1)
        self.assertEqual(len(query.get_columns(user2.id)), 4)

    def test_invalid_delete_columns(self):
        user = UserFactory()
        KanbanColumnFactory(user=user, column_number=1)
        KanbanColumnFactory(user=user, column_number=2)

        # Try deleting a column that doesn't exist
        # By the pigeonhole principle, one of these ids must be invalid ;)
        query.delete_columns([1, 2, 3])
