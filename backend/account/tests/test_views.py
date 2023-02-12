import json
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from account import business, query

class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def test_create_account(self):
        response = self.client.post(
            reverse('get_or_create_account'),
            json.dumps({'credential': 'whatever'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # The query should return the user's id. Since this is the first user in
        # the database, it has an id of 1. (This is why this test class is
        # derived from TransactionTestCase; otherwise, the id would keep
        # counting up as the other tests made users.)
        self.assertEqual(json.loads(response.content)['data'], 1)


class UpdateAccountTests(TestCase):
    def test_update_account(self):
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


    def test_invalid_account_update(self):
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


class CreateColumnTests(TestCase):
    def test_create_column(self):
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


    def test_invalid_create_column(self):
        # User doesn't exist
        response = self.client.post(
            reverse('create_column'),
            json.dumps({'google_id': '4', 'column_name': 'New column'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class GetColumnsTests(TestCase):
    def test_get_columns(self):
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


class RenameColumnTests(TestCase):
    def test_rename_column(self):
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


    def test_invalid_rename_column(self):
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


class ReorderColumnTests(TestCase):
    def test_reorder_column(self):
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


    def test_invalid_reorder_column(self):
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


class DeleteColumnTests(TestCase):
    def test_delete_column(self):
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


    def test_invalid_delete_column(self):
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


class UpdateColumnsTests(TestCase):
    def test_create_column(self):
        query.get_or_create_user({'google_id': '4'})

        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {'id': -1, 'name': 'New column', 'column_number': 0}
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        columns = json.loads(response.content)['columns']

        self.assertEqual(columns[0]['name'], 'New column')
        self.assertEqual(columns[0]['column_number'], 0)

        # Make a second column and make sure the first one is still there
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {
                        'id': columns[0]['id'],
                        'name': 'New column',
                        'column_number': 0
                    },
                    {'id': -1, 'name': 'Newer column', 'column_number': 1}
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        columns = json.loads(response.content)['columns']

        self.assertEqual(columns[0]['name'], 'New column')
        self.assertEqual(columns[0]['column_number'], 0)
        self.assertEqual(columns[1]['name'], 'Newer column')
        self.assertEqual(columns[1]['column_number'], 1)
        self.assertEqual(len(query.get_columns('4')), 2)


    def test_conflicting_new_columns(self):
        query.get_or_create_user({'google_id': '4'})

        # Creating multiple columns with the same number at the same time will
        # result in some of them being given different numbers
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {'id': -1, 'name': 'New column', 'column_number': 0},
                    # (notice the identical column_number here)
                    {'id': -1, 'name': 'Newer column', 'column_number': 0}
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        columns = json.loads(response.content)['columns']
        self.assertEqual(columns[0]['name'], 'Newer column')
        self.assertEqual(columns[0]['column_number'], 0)
        self.assertEqual(columns[1]['name'], 'New column')
        self.assertEqual(columns[1]['column_number'], 1)
        self.assertEqual(len(query.get_columns('4')), 2)


    def test_invalid_new_column(self):
        # User doesn't exist
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [{
                    'id': -1,
                    'name': 'THE column',
                    'column_number': 0
                }]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


    def test_rename(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # Rename a couple of them
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
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
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        columns = json.loads(response.content)['columns']
        self.assertEqual(columns[0]['name'], 'Old column')
        self.assertEqual(columns[0]['column_number'], 0)
        self.assertEqual(columns[1]['name'], 'The most powerful column')
        self.assertEqual(columns[1]['column_number'], 1)
        self.assertEqual(columns[2]['name'], 'Even newer column')
        self.assertEqual(columns[2]['column_number'], 2)
        self.assertEqual(len(query.get_columns('4')), 3)


    def test_reorder(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # Make the third one be the first
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {
                        'id': columns[0].id,
                        'name': 'New column',
                        'column_number': 1
                    },
                    {
                        'id': columns[1].id,
                        'name': 'Newer column',
                        'column_number': 2
                    },
                    {
                        'id': columns[2].id,
                        'name': 'Even newer column',
                        'column_number': 0
                    },
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)['columns']
        self.assertEqual(response_columns[0]['id'], columns[2].id)
        self.assertEqual(response_columns[1]['id'], columns[0].id)
        self.assertEqual(response_columns[2]['id'], columns[1].id)
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
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {
                        'id': columns[0].id,
                        'name': 'New column',
                        'column_number': 0
                    },
                    {
                        'id': columns[1].id,
                        'name': 'Newer column',
                        'column_number': 1
                    },
                    {
                        'id': columns[2].id,
                        'name': 'Even newer column',
                        'column_number': -50
                    },
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)['columns']
        self.assertEqual(response_columns[0]['id'], columns[2].id)
        self.assertEqual(response_columns[1]['id'], columns[0].id)
        self.assertEqual(response_columns[2]['id'], columns[1].id)
        self.assertEqual(len(query.get_columns('4')), 3)

        # Do the same but with the index being invalid in the other direction
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {
                        'id': columns[2].id,
                        'name': 'Even newer column',
                        'column_number': 500
                    },
                    {
                        'id': columns[0].id,
                        'name': 'New column',
                        'column_number': 0
                    },
                    {
                        'id': columns[1].id,
                        'name': 'Newer column',
                        'column_number': 1
                    },
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)['columns']
        self.assertEqual(response_columns[0]['id'], columns[0].id)
        self.assertEqual(response_columns[1]['id'], columns[1].id)
        self.assertEqual(response_columns[2]['id'], columns[2].id)
        self.assertEqual(len(query.get_columns('4')), 3)


    def test_nonexistent_user(self):
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [{
                    'id': -1,
                    'name': 'Where am I',
                    'column_number': 0
                }]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {})
