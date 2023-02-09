import json
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
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