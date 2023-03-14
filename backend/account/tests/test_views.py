import json
from unittest.mock import patch
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.http.cookie import SimpleCookie
from account.tests.factories import UserFactory, PrivacyFactory, FriendRequestFactory
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


class RemoveFriendTests(TestCase):
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


@patch("account.business.search_users_by_name")
class SearchTests(TestCase):
    def test_search_users_by_name(self, mock_search_users_by_name):
        u1 = UserFactory()
        u2 = UserFactory()
        u3 = UserFactory()
        mock_return = [u1.to_dict(), u2.to_dict(), u3.to_dict()]
        mock_search_users_by_name.return_value = mock_return

        response = self.client.post(
            reverse("search_users_by_name"),
            json.dumps("search string proxy"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content["user_list"], mock_return)


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


@patch("account.business.create_friend_request")
class CreateFriendRequestTests(TestCase):
    def test_create_friend_request_valid(self, mock_create_friend_request):
        mocked_req = FriendRequestFactory()
        mock_create_friend_request.return_value = mocked_req
        response = self.client.post(
            reverse("create_friend_request"),
            json.dumps({"from_user_id": mocked_req.from_user.id, "to_user_id": mocked_req.to_user.id}),
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, mocked_req.to_dict())

    def test_create_friend_request_error(self, mock_create_friend_request):
        mock_create_friend_request.side_effect = ObjectDoesNotExist()
        response = self.client.post(
            reverse("create_friend_request"),
            json.dumps({"from_user_id": 0, "to_user_id": 1}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        mock_create_friend_request.assert_called()


@patch("account.business.accept_friend_request")
class AcceptFriendRequestTests(TestCase):
    def test_accept_friend_request_valid(self, mock_accept_friend_request):
        mocked_req = FriendRequestFactory()
        response = self.client.post(
            reverse("accept_friend_request"),
            json.dumps(
                {
                    "request_id": mocked_req.id,
                    "to_user_id": mocked_req.to_user.id,
                    "from_user_id": mocked_req.from_user.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_accept_friend_request.assert_called_with(
            request_id=mocked_req.id, to_user_id=mocked_req.to_user.id, from_user_id=mocked_req.from_user.id
        )

    def test_accept_friend_request_error(self, mock_accept_friend_request):
        mock_accept_friend_request.side_effect = ObjectDoesNotExist()
        response = self.client.post(
            reverse("accept_friend_request"),
            json.dumps({"request_id": 0, "to_user_id": 0, "from_user_id": 0}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        mock_accept_friend_request.assert_called_with(request_id=0, to_user_id=0, from_user_id=0)


@patch("account.business.deny_friend_request")
class DenyFriendRequestTests(TestCase):
    def test_deny_friend_request_valid(self, mock_deny_friend_request):
        mocked_req = FriendRequestFactory()
        response = self.client.post(
            reverse("deny_friend_request"),
            json.dumps(
                {
                    "request_id": mocked_req.id,
                    "to_user_id": mocked_req.to_user.id,
                    "from_user_id": mocked_req.from_user.id,
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        mock_deny_friend_request.assert_called_with(
            request_id=mocked_req.id, to_user_id=mocked_req.to_user.id, from_user_id=mocked_req.from_user.id
        )

    def test_deny_friend_request_error(self, mock_deny_friend_request):
        mock_deny_friend_request.side_effect = ObjectDoesNotExist()
        response = self.client.post(
            reverse("deny_friend_request"),
            json.dumps({"request_id": 0, "to_user_id": 0, "from_user_id": 0}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        mock_deny_friend_request.assert_called_with(request_id=0, to_user_id=0, from_user_id=0)


@patch("account.business.get_friend_requests_status")
class GetFriendRequestsStatusTests(TestCase):
    def test_get_friend_requests_status_valid(self, mock_get_friend_requests_status):
        sent = [
            {"id": 0, "from_user_id": 0, "to_user_id": 0, "sent": "now", "accepted": False, "acknowledged": None},
            {"id": 1, "from_user_id": 0, "to_user_id": 0, "sent": "now", "accepted": False, "acknowledged": None},
        ]
        received = [
            {"id": 2, "from_user_id": 0, "to_user_id": 0, "sent": "now", "accepted": False, "acknowledged": None},
            {"id": 3, "from_user_id": 0, "to_user_id": 0, "sent": "later", "accepted": False, "acknowledged": None},
        ]
        mock_get_friend_requests_status.return_value = sent, received

        response = self.client.post(
            reverse("get_friend_requests_status"),
            json.dumps({"user_id": 0}),
            content_type="application/json",
        )
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["sent"], sent)
        self.assertEqual(content["received"], received)

    def test_get_friend_requests_status_error(self, mock_get_friend_requests_status):
        mock_get_friend_requests_status.side_effect = Exception()
        response = self.client.post(
            reverse("get_friend_requests_status"),
            json.dumps({"user_id": 0}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        mock_get_friend_requests_status.assert_called_with(user_id=0)
