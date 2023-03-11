import logging
import json
from django.test import TransactionTestCase
from django.urls import reverse
from unittest import mock
from django.http.cookie import SimpleCookie
from account.models import User, Privacy

logger = logging.getLogger(__name__)


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_create_account(self, mock_verify_oauth2_token):
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
        user_data = {
            "id": 1,
            "google_id": "unique_user_id",
            "username": 0,
            "image_url": "https://i.imgur.com/QJpNyuN.png",
            "last_name": "",
            "birthday": None,
            "city": None,
            "country": None,
            "region": None,
            "email": "useremail",
            "field_of_work": None,
            "first_name": "firstname",
        }
        self.assertEqual(response.status_code, 200)
        # The query should return the User object. Since a mock is used,
        # the id is as given
        self.assertEqual(
            json.loads(response.content)["data"],
            user_data,
        )

        user_data["username"] = "0"
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="unique_user_id").to_dict(),
            user_data,
        )

        # Verify User Privacy Created
        self.assertEqual(len(Privacy.objects.all()), 1)
        self.assertEqual(
            Privacy.objects.get(user__id=user_data["id"]).to_dict(),
            {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True},
        )


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class UpdateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_account(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "sub": "unique_user_id",
            "given_name": "firstname",
            "email": "useremail",
        }
        # Create an account first
        user_resp = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="unique_user_id").to_dict(),
            {
                "birthday": None,
                "city": None,
                "country": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "firstname",
                "google_id": "unique_user_id",
                "id": 1,
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "",
                "region": None,
                "username": "0",
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
            User.objects.get(google_id="unique_user_id").to_dict(),
            {
                "birthday": None,
                "city": None,
                "country": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "Rob",
                "google_id": "unique_user_id",
                "id": 1,
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "",
                "region": None,
                "username": "0",
            },
        )

    def test_invalid_account_update(self, mock_verify_oauth2_token):
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

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="unique_user_id").to_dict(),
            {
                "birthday": None,
                "city": None,
                "country": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "firstname",
                "google_id": "unique_user_id",
                "id": 1,
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "",
                "region": None,
                "username": "0",
            },
        )

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "unique_user_id", "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            User.objects.get(google_id="unique_user_id").to_dict(),
            {
                "birthday": None,
                "city": None,
                "country": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "firstname",
                "google_id": "unique_user_id",
                "id": 1,
                "image_url": "https://i.imgur.com/QJpNyuN.png",
                "last_name": "",
                "region": None,
                "username": "0",
            },
        )


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class CreatePrivacyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_get_privacies(self, mock_verify_oauth2_token):
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

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        user = json.loads(response.content)["data"]
        response = self.client.post(
            reverse("get_user_privacies"),
            json.dumps({"user_id": user["id"]}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)
        privs = json.loads(response.content)
        self.assertEqual(
            privs, {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True}
        )

    def test_invalid_get_privacies(self, mock_verify_oauth2_token):
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

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        response = self.client.post(
            reverse("get_user_privacies"),
            json.dumps({"user_id": -1}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 400)


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class UpdatePrivacyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_privacies(self, mock_verify_oauth2_token):
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

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        user = json.loads(response.content)["data"]
        self.assertEqual(
            Privacy.objects.get(user__id=user["id"]).to_dict(),
            {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True},
        )

        newPriv = {"id": 1, "is_searchable": False, "share_kanban": True, "cover_letter_requestable": False}
        # Update privacies
        response = self.client.post(
            reverse("update_privacies"),
            json.dumps({"user_id": user["id"], "privacies": newPriv}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 200)

        outPriv = Privacy.objects.get(id=1).to_dict()
        self.assertEqual(newPriv, outPriv)

    def test_invalid_update_privacies(self, mock_verify_oauth2_token):
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

        self.assertEqual(len(User.objects.all()), 1)

        # Assert that the privacies exist as default
        user = json.loads(response.content)["data"]
        self.assertEqual(
            Privacy.objects.get(user__id=user["id"]).to_dict(),
            {"id": 1, "is_searchable": True, "share_kanban": True, "cover_letter_requestable": True},
        )

        newPriv = {"id": 1, "is_searchable": False, "share_kanban": True, "cover_letter_requestable": False}
        # Update privacies
        response = self.client.post(
            reverse("update_privacies"),
            json.dumps({"user_id": -1, "privacies": newPriv}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 400)

        outPriv = Privacy.objects.get(id=1).to_dict()
        self.assertNotEqual(newPriv, outPriv)


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class AccountTestCase(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_invalid_oauth_properties(self, mock_verify_oauth2_token):
        # Try to create a user when providing an incorrect id
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "garbage", "client_id": "unusable"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)

        # No CSRF in Cookie
        self.client.cookies = SimpleCookie({"not_a_csrftoken": "not_the_droid"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)

        # No CSRF in Header
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "NOT_HTTP_X-CSRFToken": "actual_trash",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)

        # CSRFs do not match
        self.client.cookies = SimpleCookie({"csrftoken": "one_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "other_csrf_token",
        }
        # Post the request
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(Privacy.objects.all()), 0)
