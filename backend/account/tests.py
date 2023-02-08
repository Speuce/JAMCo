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


    def test_create_and_get_account_query(self):
        query.get_or_create_user({'google_id': '4'})
        # A user should exist after that query
        self.assertTrue(models.User.objects.filter(google_id='1').exists())

        # Repeating the query should result in retrieving the user, not creating
        # another one
        query.get_or_create_user({'google_id': '4'})
        self.assertTrue(models.User.objects.filter(google_id='4').exists())
        self.assertEqual(models.User.objects.filter(google_id='4').count(), 1)
