import logging
import json
from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from unittest import mock
from django.http.cookie import SimpleCookie
from .factories import UserFactory

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
        self.assertEqual(response.status_code, 200)
        # The query should return the User object. Since a mock is used,
        # the id is as given
        self.assertEqual(
            json.loads(response.content)["data"],
            {
                "id": 1,
                "google_id": "unique_user_id",
                "username": 0,
                "image_url": None,
                "last_name": "",
                "birthday": None,
                "city": None,
                "country": None,
                "region": None,
                "email": "useremail",
                "field_of_work": None,
                "first_name": "firstname",
                "last_login": None,
            },
        )


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class UpdateAccountTests(TestCase):
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

        logger.debug(f"here!: {user_resp.json()}")
        # Try updating it, the request should succeed
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"id": user_resp.json()["data"]["id"], "first_name": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

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

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": "unique_user_id", "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


@mock.patch("google.oauth2.id_token.verify_oauth2_token")
class AccountTestCase(TestCase):
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


class FriendTests(TestCase):
    @patch("account.business.add_friend")
    def test_add_friend(self, mock_add_friend):
        user1 = UserFactory()
        user2 = UserFactory()

        response = self.client.post(
            reverse("add_friend"),
            json.dumps({"user1_id": user1.id, "user2_id": user2.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_add_friend.assert_called()
        # Adding the friend again doesn't cause any problems (it's idempotent)
        response = self.client.post(
            reverse("add_friend"),
            json.dumps({"user1_id": user1.id, "user2_id": user2.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_add_friend.assert_called()

    @patch("account.business.add_friend")
    def test_invalid_add_friend(self, mock_add_friend):
        # All error handling is performed in the business and query layers, so this just checks that exceptions lead to
        # 400 errors
        def mock_add_friend_implementation(id1, id2):
            raise ValueError

        mock_add_friend.side_effect = mock_add_friend_implementation

        response = self.client.post(
            reverse("add_friend"), json.dumps({"user1_id": -1, "user2_id": -1}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        mock_add_friend.assert_called()

    @patch("account.business.remove_friend")
    def test_remove_friend(self, mock_remove_friend):
        user1 = UserFactory()
        user2 = UserFactory()

        response = self.client.post(
            reverse("remove_friend"),
            json.dumps({"user1_id": user1.id, "user2_id": user2.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_remove_friend.assert_called()

        # Removing the friend again is idempotent too
        response = self.client.post(
            reverse("remove_friend"),
            json.dumps({"user1_id": user1.id, "user2_id": user2.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_remove_friend.assert_called()

    @patch("account.business.remove_friend")
    def test_invalid_remove_friend(self, mock_remove_friend):
        # Like test_invalid_add_friend, we're just making sure exceptions lead to errors
        def mock_remove_friend_implementation(id1, id2):
            raise ValueError

        mock_remove_friend.side_effect = mock_remove_friend_implementation

        response = self.client.post(
            reverse("remove_friend"), json.dumps({"user1_id": -1, "user2_id": -1}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        mock_remove_friend.assert_called()
