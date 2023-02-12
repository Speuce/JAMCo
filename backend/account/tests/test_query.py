from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from account import query, models

class GetOrCreateTests(TestCase):
    def test_create_and_get_account(self):
        query.get_or_create_user({'google_id': '4'})
        # A user should exist after that query
        self.assertTrue(models.User.objects.filter(google_id='4').exists())

        # Repeating the query should result in retrieving the user, not creating
        # another one
        query.get_or_create_user({'google_id': '4'})
        self.assertTrue(models.User.objects.filter(google_id='4').exists())
        self.assertEqual(models.User.objects.filter(google_id='4').count(), 1)


class UserExistsTests(TestCase):
    def test_user_exists(self):
        self.assertFalse(query.user_exists('4'))
        query.get_or_create_user({'google_id': '4'})
        self.assertTrue(query.user_exists('4'))


class UpdateAccountTests(TestCase):
    def test_update_account(self):
        # Create an account first
        query.get_or_create_user({'google_id': '4'})

        # Update the user
        query.update_user({'google_id': '4', 'first_name': 'Rob'})

        # The modifications should hold
        self.assertEqual(
            query.get_or_create_user({'google_id': '4'}).first_name, 'Rob')


    def test_invalid_update_account(self):
        # Create an account first
        query.get_or_create_user({'google_id': '4'})

        # "Update" the user
        with self.assertRaises(AttributeError):
            query.update_user({'google_id': '4', 'favourite_prof': 'Rasit'})

        # Update the "user"
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.update_user({
                'google_id': '41 6D 6F 6E 67 20 55 73', 'first_name': 'Rob'})
        # User not specified
        with self.assertRaises(KeyError):
            query.update_user({'first_name': 'Rob'})


class CreateColumnTests(TestCase):
    def test_create_column(self):
        query.get_or_create_user({'google_id': '4'})
        new_column = query.create_column('4', 'New column')
        newer_column = query.create_column('4', 'Newer column')

        # Column numbers should be in order of creation by default
        self.assertEqual(new_column.column_number, 0)
        self.assertEqual(newer_column.column_number, 1)


    def test_duplicate_column_names(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')
        query.create_column('4', 'Newer column')

        # Duplicate names are allowed
        duplicate_name_column = query.create_column('4', 'Newer column')
        self.assertEqual(duplicate_name_column.column_number, 2)


    def test_invalid_create_column(self):
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.create_column('4', 'New column')


class GetColumnsTests(TestCase):
    def test_get_columns(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')
        query.create_column('4', 'Newest column')
        query.create_column('4', 'Newester column')
        # Make another user
        query.get_or_create_user({'google_id': '5'})
        query.create_column('5', 'New column')
        query.create_column('5', 'Newest column')
        query.create_column('5', 'Newester column')
        query.create_column('5', 'Newesterest column')

        columns = query.get_columns('4')

        # The query should only return the columns for the specified user
        self.assertEqual(columns.count(), 3)
        for column in columns:
            self.assertEqual(column.user.google_id, '4')


class RenameColumnTests(TestCase):
    def test_rename_column(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')
        query.create_column('4', 'Newest column')
        query.create_column('4', 'Newester column')

        query.rename_column('4', 1, 'Renamed')

        renamed_column = models.KanbanColumn.objects.get(
            user=query.get_or_create_user({'google_id': '4'}), column_number=1)
        self.assertEqual(renamed_column.name, 'Renamed')


    def test_invalid_rename_column(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')

        # Try renaming a column that doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.rename_column('4', 1, 'Totally real column')

        # Try renaming a column for a user that doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.rename_column('53 55 53 53 59', 1, 'This is real I promise')


class DeleteColumnTests(TestCase):
    def test_delete_column(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')

        query.delete_column('4', 0)
        self.assertEqual(len(query.get_columns('4')), 0)


    def test_invalid_delete_column(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'uhh')

        # Column number too low
        with self.assertRaises(ObjectDoesNotExist):
            query.delete_column('4', -1)
        # Column number too high
        with self.assertRaises(ObjectDoesNotExist):
            query.delete_column('4', 1)
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.delete_column('IIII', 0)


    def test_delete_columns(self):
        query.get_or_create_user({'google_id': '4'})
        column1 = query.create_column('4', 'New column')
        column2 = query.create_column('4', 'Newest column')
        query.create_column('4', 'Newester column')
        # Make another user
        query.get_or_create_user({'google_id': '5'})
        query.create_column('5', 'New column')
        query.create_column('5', 'Newest column')
        query.create_column('5', 'Newester column')
        query.create_column('5', 'Newesterest column')

        query.delete_columns([column1.id, column2.id])
        self.assertEqual(len(query.get_columns('4')), 1)
        self.assertEqual(len(query.get_columns('5')), 4)

