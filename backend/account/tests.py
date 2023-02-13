import json
from unittest import mock
from django.http.cookie import SimpleCookie
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from . import query, models


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class AccountTestCase(TestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_create_account_view(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        # The query should return the User object. Since a mock is used,
        # the id is as given
        self.assertEqual(
            json.loads(response.content)["data"],
            {
                "google_id": "unique_user_id",
                "username": 0,
                "image_url": None,
                "last_name": "No Last Name Found",
                "birthday": None,
                "city": None,
                "country": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "firstname",
                "last_login": None,
            },
        )

    def test_update_account_view(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        # Create an account first
        self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )

        # Try updating it, the request should succeed
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "unique_user_id", "first_name": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_account_update_view(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        # Create an account first
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "unique_user_id", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "unique_user_id", "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_and_get_account_query(self, mock_verify_oauth2_token):
        # 'sub' is the field name from google tokens
        query.get_or_create_user({"sub": "4"})
        # A user should exist after that query
        self.assertTrue(models.User.objects.filter(google_id="4").exists())

        # Repeating the query should result in retrieving the user, not creating
        # another one
        query.get_or_create_user({"sub": "4"})
        self.assertTrue(models.User.objects.filter(google_id="4").exists())
        self.assertEqual(models.User.objects.filter(google_id="4").count(), 1)

    def test_update_account_query(self, mock_verify_oauth2_token):
        # Create an account first # 'sub' is the field name from google tokens
        query.get_or_create_user({"sub": "4"})

        # Update the user
        query.update_user({"google_id": "4", "first_name": "Rob"})

        # The modifications should hold
        self.assertEqual(query.get_or_create_user({"sub": "4"}).first_name, "Rob")

    def test_invalid_update_account_query(self, mock_verify_oauth2_token):
        # Create an account first # 'sub' is the field name from google tokens
        query.get_or_create_user({"sub": "4"})

        # "Update" the user
        with self.assertRaises(AttributeError):
            query.update_user({"google_id": "4", "favourite_prof": "Rasit"})

        # Update the "user"
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.update_user(
                {"google_id": "41 6D 6F 6E 67 20 55 73", "first_name": "Rob"}
            )
        # User not specified
        with self.assertRaises(KeyError):
            query.update_user({"first_name": "Rob"})

    def test_invalid_oauth_properties(self, mock_verify_oauth2_token):
        # Try to create a user when providing an incorrect id
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "garbage", "client_id": "unusable"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
