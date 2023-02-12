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
        query.create_column('4', 'New column')
        query.create_column('4', 'Newest column')
        query.create_column('4', 'Newester column')

        columns = business.get_columns('4')
        column_numbers = [column.column_number for column in columns]
        # Returned columns should be sorted by column number
        self.assertTrue(all(
            column_numbers[i] <= column_numbers[i+1]
            for i in range(len(column_numbers) - 1)
        ))


class UpdateColumnsTests(TestCase):
    def test_conflicting_new_columns(self):
        query.get_or_create_user({'google_id': '4'})

        # Creating multiple columns with the same number at the same time will
        # result in some of them being given different numbers
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'New column', 'column_number': 0},
        ])

        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0].name, 'New column')
        self.assertEqual(columns[0].column_number, 0)
        self.assertEqual(columns[1].name, 'New column')
        self.assertEqual(columns[1].column_number, 1)


    def test_rename(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # Rename the first two
        columns = business.update_columns('4', [
            {
                'id': columns[0].id,
                'name': 'Old column',
                'column_number': 0
            },
            {
                'id': columns[1].id,
                'name': 'The most powerful column',
                'column_number': 1
            },
            {
                'id': columns[2].id,
                'name': 'Even newer column',
                'column_number': 2
            },
        ])

        self.assertEqual(columns[0].name, 'Old column')
        self.assertEqual(columns[0].column_number, 0)
        self.assertEqual(columns[1].name, 'The most powerful column')
        self.assertEqual(columns[1].column_number, 1)
        self.assertEqual(columns[2].name, 'Even newer column')
        self.assertEqual(columns[2].column_number, 2)
        self.assertEqual(len(query.get_columns('4')), 3)


    def test_reorder(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # Make the third one be the first
        result_columns = business.update_columns('4', [
            {'id': columns[0].id, 'name': 'New column', 'column_number': 1},
            {'id': columns[1].id,'name': 'Newer column','column_number': 2},
            {
                'id': columns[2].id,
                'name': 'Even newer column',
                'column_number': 0
            }
        ])

        self.assertEqual(result_columns[0].id, columns[2].id)
        self.assertEqual(result_columns[1].id, columns[0].id)
        self.assertEqual(result_columns[2].id, columns[1].id)
        self.assertEqual(len(query.get_columns('4')), 3)


    def test_out_of_bounds_reorder(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # Make the third one be the first. Er, the one at index negative-fifty.
        # It should be treated as index zero anyway.
        result_columns = business.update_columns('4', [
            {'id': columns[0].id, 'name': 'New column', 'column_number': 1},
            {'id': columns[1].id, 'name': 'Newer column', 'column_number': 2},
            {
                'id': columns[2].id,
                'name': 'Even newer column',
                'column_number': -50
            },
        ])

        self.assertEqual(result_columns[0].id, columns[2].id)
        self.assertEqual(result_columns[1].id, columns[0].id)
        self.assertEqual(result_columns[2].id, columns[1].id)
        self.assertEqual(len(query.get_columns('4')), 3)

        # Do the same but with the index being invalid in the other direction
        result_columns = business.update_columns('4', [
            {
                'id': columns[0].id,
                'name': 'Even newer column',
                'column_number': 500
            },
            {'id': columns[1].id, 'name': 'New column', 'column_number': 0},
            {'id': columns[2].id, 'name': 'Newer column', 'column_number': 1},
        ])

        self.assertEqual(result_columns[0].id, columns[1].id)
        self.assertEqual(result_columns[1].id, columns[2].id)
        self.assertEqual(result_columns[2].id, columns[0].id)
        self.assertEqual(len(query.get_columns('4')), 3)


    def test_delete(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        result_columns = business.update_columns('4', [
            {
                'id': columns[2].id,
                'name': 'Even newer column',
                'column_number': 2
            },
            {'id': columns[0].id, 'name': 'New column', 'column_number': 0},
        ])

        # Since column 1 was absent from the update request, it should be gone
        self.assertEqual(result_columns[0].id, columns[0].id)
        self.assertEqual(result_columns[1].id, columns[2].id)
        self.assertEqual(len(query.get_columns('4')), 2)


    def test_nonexistent_user(self):
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            business.update_columns('4', [
                {'id': -1, 'name': 'New column', 'column_number': 0},
                {'id': -1, 'name': 'New column', 'column_number': 1},
            ])


    def test_empty_payload(self):
        query.get_or_create_user({'google_id': '4'})
        business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # If the user has columns, an empty update should delete all of them
        result_columns = business.update_columns('4', [])
        self.assertEqual(len(result_columns), 0)
        self.assertEqual(len(query.get_columns('4')), 0)

        # After that, an empty update shouldn't do anything
        result_columns = business.update_columns('4', [])
        self.assertEqual(len(result_columns), 0)
        self.assertEqual(len(query.get_columns('4')), 0)
