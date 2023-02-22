from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from account.query import get_or_create_user
from column import query


class CreateColumnTests(TestCase):
    def test_create_column(self):
        user = get_or_create_user({"sub": "4"})
        new_column = query.create_column(user.id, "New column", 0)
        newer_column = query.create_column(user.id, "Newer column", 1)

        # Column numbers should be in order of creation by default
        self.assertEqual(new_column.column_number, 0)
        self.assertEqual(newer_column.column_number, 1)

    def test_duplicate_column_names(self):
        user = get_or_create_user({"sub": "4"})
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
        user = get_or_create_user({"sub": "4"})
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newest column", 1)
        query.create_column(user.id, "Newester column", 2)
        # Make another user
        user2 = get_or_create_user({"sub": "5"})
        query.create_column(user2.id, "New column", 0)
        query.create_column(user2.id, "Newest column", 1)
        query.create_column(user2.id, "Newester column", 2)
        query.create_column(user2.id, "Newesterest column", 3)

        columns = query.get_columns(user.id)

        # The query should only return the columns for the specified user
        self.assertEqual(columns.count(), 3)
        for column in columns:
            self.assertEqual(column.user.id, user.id)


class DeleteColumnsTests(TestCase):
    def test_delete_column(self):
        user = get_or_create_user({"sub": "4"})
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newester column", 1)

        query.delete_column(user.id, 0)
        self.assertEqual(len(query.get_columns(user.id)), 1)

    def test_delete_columns(self):
        user = get_or_create_user({"sub": "4"})
        column1 = query.create_column(user.id, "New column", 0)
        column2 = query.create_column(user.id, "Newest column", 1)
        query.create_column(user.id, "Newester column", 2)
        # Make another user
        user2 = get_or_create_user({"sub": "5"})
        query.create_column(user2.id, "New column", 0)
        query.create_column(user2.id, "Newest column", 1)
        query.create_column(user2.id, "Newester column", 2)
        query.create_column(user2.id, "Newesterest column", 3)

        query.delete_columns([column1.id, column2.id])
        self.assertEqual(len(query.get_columns(user.id)), 1)
        self.assertEqual(len(query.get_columns(user2.id)), 4)

    def test_invalid_delete_columns(self):
        user = get_or_create_user({"sub": "4"})
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newest column", 1)

        # Try deleting a column that doesn't exist
        # By the pigeonhole principle, one of these ids must be invalid ;)
        query.delete_columns([1, 2, 3])
