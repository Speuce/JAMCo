import logging
import json
from django.test import TransactionTestCase
from django.urls import reverse
from django.http.cookie import SimpleCookie
from account.models import User

logger = logging.getLogger(__name__)


class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_create_account(self):
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        user_data = {
            "id": 1,
            "google_id": "1234567890",
            "username": "1234567890",
            "image_url": "https://i.imgur.com/QJpNyuN.png",
            "last_name": "Doe",
            "birthday": None,
            "city": None,
            "country": None,
            "region": None,
            "email": "john.doe@gmail.com",
            "field_of_work": None,
            "first_name": "John",
        }
        self.assertEqual(response.status_code, 200)
        # The query should return the User object. Since a mock is used,
        # the id is as given
        self.assertEqual(
            json.loads(response.content)["data"],
            user_data,
        )

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            user_data,
        )


class UpdateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_account(self):
        # Create an account first
        user_resp = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "1234567890",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "John",
            },
        )

        # Try updating it, the request should succeed
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"id": user_resp.json()["data"]["id"], "first_name": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "1234567890",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "Rob",
            },
        )

    def test_invalid_account_update(self):
        # Create an account first
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "1234567890",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "John",
            },
        )

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "1234567890", "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="1234567890").to_dict(),
            {
                "id": 1,
                "google_id": "1234567890",
                "username": "1234567890",
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "Doe",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "john.doe@gmail.com",
                "field_of_work": None,
                "first_name": "John",
            },
        )


class AccountTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_invalid_oauth_properties(self):
        # Try to create a user when providing an incorrect id
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "garbage", "client_id": "unusable"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)

        # No CSRF in Cookie
        self.client.cookies = SimpleCookie({"not_a_csrftoken": "not_the_droid"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)

        # No CSRF in Header
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "NOT_HTTP_X-CSRFToken": "actual_trash",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)

        # CSRFs do not match
        self.client.cookies = SimpleCookie({"csrftoken": "one_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "other_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
