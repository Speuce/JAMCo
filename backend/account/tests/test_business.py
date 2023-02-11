from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from account import business, query

class CreateUserTests(TestCase):
    def test_create_user(self):
        # Make sure default columns are created
        business.get_or_create_user({'google_id': '4'})
        columns = business.get_columns('4')
        self.assertEqual(columns[0].name, "To Apply")
        self.assertEqual(columns[1].name, "Application Submitted")
        self.assertEqual(columns[2].name, "OA")
        self.assertEqual(columns[3].name, "Interview")


class GetColumnsTests(TestCase):
    def test_get_columns(self):
        # Using the query function for creating a user means that we don't have
        # to worry about the default columns
        query.get_or_create_user({'google_id': '4'})
        business.create_column('4', 'New column')
        business.create_column('4', 'Newest column')
        business.create_column('4', 'Newester column')

        columns = business.get_columns('4')
        column_numbers = [column.column_number for column in columns]
        # Returned columns should be sorted by column number
        self.assertTrue(all(
            column_numbers[i] <= column_numbers[i+1]
            for i in range(len(column_numbers) - 1)
        ))


class ReorderColumnTests(TestCase):
    def test_reorder_column(self):
        query.get_or_create_user({'google_id': '4'})
        column2 = business.create_column('4', 'Should be the second column')
        column1 = business.create_column('4', 'Should be the first column')
        business.create_column('4', 'Should be the third column')

        changed_columns = business.reorder_column('4', 0, 1)
        self.assertEqual(changed_columns, [column1, column2])


    def test_invalid_reorder_column(self):
        query.get_or_create_user({'google_id': '4'})
        business.create_column('4', 'Should be the first column')
        business.create_column('4', 'Should be the second column')

        with self.assertRaises(ValueError):
            business.reorder_column('4', 1, 9999)

        with self.assertRaises(ValueError):
            business.reorder_column('4', 2, 0)

        with self.assertRaises(ValueError):
            business.reorder_column('4', -1, 0)

        with self.assertRaises(ObjectDoesNotExist):
            business.reorder_column('FFFF', 1, 0)


class DeleteColumnTests(TestCase):
    def test_delete_column(self):
        query.get_or_create_user({'google_id': '4'})
        business.create_column('4', 'column')
        column2 = business.create_column('4', 'COLUMN')
        column3 = business.create_column('4', 'Row >:)')

        changed_columns = business.delete_column('4', 0)
        self.assertEqual(changed_columns, [column2, column3])

        column2.refresh_from_db()
        column3.refresh_from_db()

        self.assertEqual(column2.column_number, 0)
        self.assertEqual(column3.column_number, 1)
        self.assertEqual(len(query.get_columns('4')), 2)