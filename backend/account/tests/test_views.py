import json
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from unittest.mock import patch
from django.http.cookie import SimpleCookie
from account.tests.factories import UserFactory


class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    @patch("google.oauth2.id_token.verify_oauth2_token")
    @patch("account.business.get_or_create_user")
    def test_create_account(self, mock_get_or_create_user, mock_verify_oauth2_token):
        mocked_user = UserFactory()
        mock_get_or_create_user.return_value = mocked_user, True

        mock_verify_oauth2_token.return_value = {
            "sub": mocked_user.google_id,
            "given_name": mocked_user.first_name,
            "email": mocked_user.email,
        }

        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "whatever", "client_id": "8675309"}),
            content_type="application/json",
            **self.header,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content)["data"], mocked_user.to_dict())


@patch("account.business.update_user")
class UpdateAccountTests(TestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_update_account(self, mock_update_user):
        user = UserFactory()

        # Try updating it, the request should succeed
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"id": user.id, "first_name": "Rob"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_update_user.assert_called_with({"id": user.id, "first_name": "Rob"})

    def test_invalid_account_update(self, mock_update_user):
        user = UserFactory()
        mock_update_user.side_effect = AttributeError("User has no attribute " + "favourite_prof")

        # Should fail if the given fields don't exist
        response = self.client.post(
            reverse("update_account"),
            json.dumps({"google_id": user.google_id, "favourite_prof": "Rob"}),
            content_type="application/json",
        )
        mock_update_user.assert_called_with({"google_id": user.google_id, "favourite_prof": "Rob"})
        self.assertEqual(response.status_code, 400)


@patch("account.business.get_or_create_user")
class AccountTestCase(TestCase):
    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    def test_invalid_oauth_properties(self, mock_get_or_create_user):
        # Try to create a user when providing an incorrect id
        response = self.client.post(
            reverse("get_or_create_account"),
            json.dumps({"credential": "garbage", "client_id": "unusable"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)
        mock_get_or_create_user.assert_not_called()

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
        mock_get_or_create_user.assert_not_called()

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
        mock_get_or_create_user.assert_not_called()

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
        mock_get_or_create_user.assert_not_called()
