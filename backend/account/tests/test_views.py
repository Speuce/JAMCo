import json
from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.http.cookie import SimpleCookie
from account.tests.factories import UserFactory, PrivacyFactory
from django.core.exceptions import ObjectDoesNotExist


class GetOrCreateAccountTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.client.cookies = SimpleCookie({"csrftoken": "valid_csrf_token"})
        self.header = {
            "ACCEPT": "application/json",
            "HTTP_X-CSRFToken": "valid_csrf_token",
        }

    @patch("account.stubs.stub_verify_oauth2_token")
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
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )

        self.assertEqual(json.loads(response.data)["error"], None)

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
            json.dumps({"credential": "test", "client_id": "test"}),
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
            json.dumps({"credential": "test", "client_id": "test"}),
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
            json.dumps({"credential": "test", "client_id": "test"}),
            content_type="application/json",
            **self.header,
        )
        self.assertEqual(response.status_code, 401)

        mock_get_or_create_user.assert_not_called()


class PrivacyTests(TestCase):
    @patch("account.business.update_privacies")
    def test_update_privacies(self, mock_update_privacies):
        priv = PrivacyFactory()
        newPrivDict = {
            "is_searchable": False,
            "share_kanban": True,
            "cover_letter_requestable": False,
        }

        response = self.client.post(
            reverse("update_privacies"),
            json.dumps({"user_id": priv.user.id, "privacies": newPrivDict}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_update_privacies.assert_called_with({"user_id": priv.user.id, "privacies": newPrivDict})

    @patch("account.business.update_privacies")
    def test_invalid_update_privacies(self, mock_update_privacies):
        priv = PrivacyFactory()
        newPrivDict = {
            # invalid name
            "searchable": False,
            "share_kanban": True,
            "cover_letter_requestable": False,
        }
        mock_update_privacies.side_effect = AttributeError

        response = self.client.post(
            reverse("update_privacies"),
            json.dumps({"user_id": priv.user.id, "privacies": newPrivDict}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        mock_update_privacies.assert_called_with({"user_id": priv.user.id, "privacies": newPrivDict})

    @patch("account.business.get_privacies")
    def test_get_user_privacies(self, mock_get_privacies):
        priv = PrivacyFactory()
        mock_get_privacies.return_value = priv

        response = self.client.post(
            reverse("get_user_privacies"),
            json.dumps({"user_id": priv.user.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_get_privacies.assert_called_with(priv.user.id)

    @patch("account.business.get_privacies")
    def test_invalid_get_user_privacies(self, mock_get_privacies):
        mock_get_privacies.side_effect = Exception

        response = self.client.post(
            reverse("get_user_privacies"),
            json.dumps({"user_id": -1}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


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


@patch("account.business.authenticate_token")
class AuthenticateTokenTests(TestCase):
    def test_validate_auth_token(self, mock_authenticate_token):
        user = UserFactory()
        mock_authenticate_token.return_value = user, "encrypted_token"
        response = self.client.post(
            reverse("validate_auth_token"), json.dumps({"token": "valid_token"}), content_type="application/json"
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        mock_authenticate_token.assert_called()
        self.assertEqual(content["user"], user.to_dict())
        self.assertEqual(content["token"], "encrypted_token")

    def test_validate_auth_token_invalid(self, mock_authenticate_token):
        mock_authenticate_token.side_effect = ObjectDoesNotExist("Invalid Token")
        response = self.client.post(
            reverse("validate_auth_token"), json.dumps({"token": "invalid_token"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        mock_authenticate_token.assert_called()
