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

        response_columns = json.loads(response.content)['columns']
        self.assertEqual(response_columns[0]['name'], 'New column')
        self.assertEqual(response_columns[0]['column_number'], 0)
        self.assertEqual(response_columns[1]['name'], 'Newer column')
        self.assertEqual(response_columns[1]['column_number'], 1)
        self.assertEqual(response_columns[2]['name'], 'Even newer column')
        self.assertEqual(response_columns[2]['column_number'], 2)
        self.assertEqual(len(query.get_columns('4')), 3)

        self.assertEqual(response.status_code, 200)


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


    def test_invalid_request(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # User doesn't exist
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '5',
                'payload': [{
                    'id': columns[0].id,
                    'name': 'THE column',
                    'column_number': 0
                }]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        # Make sure the request didn't update anything
        self.assertEqual(business.get_columns('4')[0].name, 'New column')


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
                    {
                        'id': columns[2].id,
                        'name': 'Even newer column',
                        'column_number': 2
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


    def test_delete(self):
        query.get_or_create_user({'google_id': '4'})
        columns = business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        response = self.client.post(
            reverse('update_columns'),
            json.dumps({
                'google_id': '4',
                'payload': [
                    {
                        'id': columns[2].id,
                        'name': 'Even newer column',
                        'column_number': 2
                    },
                    {
                        'id': columns[0].id,
                        'name': 'New column',
                        'column_number': 0
                    },
                ]
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)['columns']
        # Since column 1 was absent from the update request, it should be gone
        self.assertEqual(response_columns[0]['id'], columns[0].id)
        self.assertEqual(response_columns[1]['id'], columns[2].id)
        self.assertEqual(len(query.get_columns('4')), 2)


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


    def test_empty_payload(self):
        query.get_or_create_user({'google_id': '4'})
        business.update_columns('4', [
            {'id': -1, 'name': 'New column', 'column_number': 0},
            {'id': -1, 'name': 'Newer column', 'column_number': 1},
            {'id': -1, 'name': 'Even newer column', 'column_number': 2},
        ])

        # If the user has columns, an empty update should delete all of them
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({'google_id': '4', 'payload': []}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)['columns']
        self.assertEqual(len(response_columns), 0)
        self.assertEqual(len(query.get_columns('4')), 0)

        # After that, an empty update shouldn't do anything
        response = self.client.post(
            reverse('update_columns'),
            json.dumps({'google_id': '4', 'payload': []}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_columns = json.loads(response.content)['columns']
        self.assertEqual(len(response_columns), 0)
        self.assertEqual(len(query.get_columns('4')), 0)
