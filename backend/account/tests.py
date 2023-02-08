import json
from django.test import TestCase
from django.urls import reverse
from . import query, models

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
        self.assertEqual(response.content['data'], 1)
