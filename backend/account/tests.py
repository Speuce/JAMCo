import json
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from . import business, query, models

class AccountTestCase(TestCase):
    def setUp(self):
        pass


    def test_create_account_view(self):
        response = self.client.post(
            reverse('get_or_create_account'),
            json.dumps({'credential': 'whatever'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # The query should return the user's id. Since this is the first user in
        # the database, it has an id of 1.
        self.assertEqual(json.loads(response.content)['data'], 1)


    def test_update_account_view(self):
        # Create an account first
        self.client.post(
            reverse('get_or_create_account'),
            json.dumps({'credential': 'whatever'}),
            content_type='application/json'
        )

        # Try updating it, the request should succeed
        response = self.client.post(
            reverse('update_account'),
            json.dumps({'google_id': 'whatever', 'first_name': 'Rob'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)


    def test_invalid_account_update_view(self):
        # Create an account first
        self.client.post(
            reverse('get_or_create_account'),
            json.dumps({'credential': 'whatever'}),
            content_type='application/json'
        )

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse('update_account'),
            json.dumps({'google_id': 'whatever', 'favourite_prof': 'Rob'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


    def test_create_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        response = self.client.post(
            reverse('create_column'),
            json.dumps({'google_id': '4', 'column_name': 'New column'}),
            content_type='application/json'
        )

        self.assertEqual(
            json.loads(response.content),
            {'name': 'New column', 'column_number': 0}
        )
        self.assertEqual(response.status_code, 200)


    def test_invalid_create_column_view(self):
        # User doesn't exist
        response = self.client.post(
            reverse('create_column'),
            json.dumps({'google_id': '4', 'column_name': 'New column'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


    def test_get_columns_view(self):
        query.get_or_create_user({'google_id': '4'})
        # Make several columns
        query.create_column('4', 'New column')
        query.create_column('4', 'Newer column')
        query.create_column('4', 'Even newer column')

        response = self.client.post(
            reverse('get_columns'),
            json.dumps({'google_id': '4'}),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response.content)['columns'],
            [
                {'name': 'New column', 'column_number': 0},
                {'name': 'Newer column', 'column_number': 1},
                {'name': 'Even newer column', 'column_number': 2}
            ]
        )
        self.assertEqual(response.status_code, 200)


    def test_rename_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        # Make several columns
        query.create_column('4', 'New column')
        query.create_column('4', 'Newer column')
        query.create_column('4', 'Even newer column')

        # Rename a couple of them
        response1 = self.client.post(
            reverse('rename_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 0,
                'new_name': 'Old column'
            }),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(
            json.loads(response1.content),
            {'column': {'name': 'Old column', 'column_number': 0}},
        )

        response2 = self.client.post(
            reverse('rename_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 1,
                'new_name': 'The most powerful column'
            }),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            json.loads(response2.content),
            {
                'column': {
                    'name': 'The most powerful column',
                    'column_number': 1
                }
            },
        )

        # Make sure all changes are reflected when we get all columns
        response3 = self.client.post(
            reverse('get_columns'),
            json.dumps({'google_id': '4'}),
            content_type='application/json'
        )
        self.assertEqual(
            json.loads(response3.content),
            { 'columns':
                [
                    {'name': 'Old column', 'column_number': 0},
                    {'name': 'The most powerful column', 'column_number': 1},
                    {'name': 'Even newer column', 'column_number': 2}
                ]
            }
        )


    def test_invalid_rename_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')

        # Try renaming a column that doesn't exist
        response1 = self.client.post(
            reverse('rename_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 1,
                'new_name': 'Totally real column'
            }),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 400)
        self.assertEqual(json.loads(response1.content), {})

        # Try renaming a column for a user that doesn't exist
        response3 = self.client.post(
            reverse('rename_column'),
            json.dumps({
                'google_id': '53 55 53',
                'column_number': 1,
                'new_name': 'Totally real column'
            }),
            content_type='application/json'
        )
        self.assertEqual(response3.status_code, 400)
        self.assertEqual(json.loads(response3.content), {})


    def test_reorder_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'Should be the second column')
        query.create_column('4', 'Should be the first column')
        query.create_column('4', 'Should be the third column')
        # Oh no! The columns are in the wrong order!
        response = self.client.post(
            reverse('reorder_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 1,
                'new_column_number': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # It should return the columns that were changed
        self.assertEqual(
            json.loads(response.content),
            {'changed_columns':
                [
                    {'name': 'Should be the first column', 'column_number': 0},
                    {'name': 'Should be the second column', 'column_number': 1},
                ]
            }
        )


    def test_invalid_reorder_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'Should be the first column')
        query.create_column('4', 'Should be the second column')

        # This isn't how you delete a column >:(
        response = self.client.post(
            reverse('reorder_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 1,
                'new_column_number': 99999999999
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})

        # Source column doesn't exist
        response = self.client.post(
            reverse('reorder_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 2,
                'new_column_number': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})
        # Source column doesn't exist, but it's out of range on the other end
        response = self.client.post(
            reverse('reorder_column'),
            json.dumps({
                'google_id': '4',
                'column_number': -1,
                'new_column_number': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})

        # User doesn't exist
        response = self.client.post(
            reverse('reorder_column'),
            json.dumps({
                'google_id': 'four',
                'column_number': 1,
                'new_column_number': 0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})


    def test_delete_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'First column')
        query.create_column('4', 'To be deleted')
        query.create_column('4', 'To be second')

        response = self.client.post(
            reverse('delete_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 1,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'changed_columns': [{'name': 'To be second', 'column_number': 1}]}
        )
        self.assertEqual(len(business.get_columns('4')), 2)


    def test_invalid_delete_column_view(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', "Pwease don't dewete me 🥺")

        # Column number too low
        response = self.client.post(
            reverse('delete_column'),
            json.dumps({
                'google_id': '4',
                'column_number': -1,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})
        self.assertEqual(len(business.get_columns('4')), 1)

        # Column number too high
        response = self.client.post(
            reverse('delete_column'),
            json.dumps({
                'google_id': '4',
                'column_number': 1,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})
        self.assertEqual(len(business.get_columns('4')), 1)

        # User doesn't exist
        response = self.client.post(
            reverse('delete_column'),
            json.dumps({
                'google_id': 'IV',
                'column_number': -1,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})
        self.assertEqual(len(business.get_columns('4')), 1)


    def test_get_columns_business(self):
        business.get_or_create_user({'google_id': '4'})
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


    def test_reorder_column_business(self):
        business.get_or_create_user({'google_id': '4'})
        column2 = business.create_column('4', 'Should be the second column')
        column1 = business.create_column('4', 'Should be the first column')
        business.create_column('4', 'Should be the third column')

        changed_columns = business.reorder_column('4', 0, 1)
        self.assertEqual(changed_columns, [column1, column2])


    def test_invalid_reorder_column_business(self):
        business.get_or_create_user({'google_id': '4'})
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


    def test_delete_column_business(self):
        business.get_or_create_user({'google_id': '4'})
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


    def test_create_and_get_account_query(self):
        query.get_or_create_user({'google_id': '4'})
        # A user should exist after that query
        self.assertTrue(models.User.objects.filter(google_id='4').exists())

        # Repeating the query should result in retrieving the user, not creating
        # another one
        query.get_or_create_user({'google_id': '4'})
        self.assertTrue(models.User.objects.filter(google_id='4').exists())
        self.assertEqual(models.User.objects.filter(google_id='4').count(), 1)


    def test_update_account_query(self):
        # Create an account first
        query.get_or_create_user({'google_id': '4'})

        # Update the user
        query.update_user({'google_id': '4', 'first_name': 'Rob'})

        # The modifications should hold
        self.assertEqual(
            query.get_or_create_user({'google_id': '4'}).first_name, 'Rob')


    def test_invalid_update_account_query(self):
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


    def test_create_column_query(self):
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


    def test_invalid_create_column_query(self):
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.create_column('4', 'New column')


    def test_get_columns_query(self):
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


    def test_rename_column_query(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')
        query.create_column('4', 'Newest column')
        query.create_column('4', 'Newester column')

        query.rename_column('4', 1, 'Renamed')

        renamed_column = models.KanbanColumn.objects.get(
            user=query.get_or_create_user({'google_id': '4'}), column_number=1)
        self.assertEqual(renamed_column.name, 'Renamed')


    def test_invalid_rename_column_query(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')

        # Try renaming a column that doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.rename_column('4', 1, 'Totally real column')

        # Try renaming a column for a user that doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.rename_column('53 55 53 53 59', 1, 'This is real I promise')


    def test_delete_column_query(self):
        query.get_or_create_user({'google_id': '4'})
        query.create_column('4', 'New column')

        changed_columns = query.delete_column('4', 0)
        self.assertEqual(len(query.get_columns('4')), 0)


    def test_invalid_delete_column_query(self):
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
