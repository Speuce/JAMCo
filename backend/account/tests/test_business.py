from django.test import TestCase
from account import business
from unittest.mock import patch
from account.tests.factories import UserFactory, PrivacyFactory, FriendRequestFactory
from django.core.exceptions import ObjectDoesNotExist


@patch("account.business.encrypt_token")
@patch("account.query.get_or_create_user")
@patch("account.query.user_exists")
@patch("account.business.create_default_columns")
class GetOrCreateUserTests(TestCase):
    def test_get_or_create_user_new(
        self, mock_create_default_columns, mock_user_exists, mock_get_or_create_user, mock_encrypt_token
    ):
        mocked_user = UserFactory()
        mock_get_or_create_user.return_value = mocked_user
        mock_user_exists.return_value = False
        mock_encrypt_token.return_value = "encrypted_token"

        user, token = business.get_or_create_user({"sub": mocked_user.google_id})
        self.assertEqual(mocked_user.to_dict(), user.to_dict())
        self.assertEqual(token, "encrypted_token")

        # Make sure default columns are created
        mock_create_default_columns.assert_called_with(mocked_user.id)

    def test_get_or_create_user_existing(
        self, mock_create_default_columns, mock_user_exists, mock_get_or_create_user, mock_encrypt_token
    ):
        mocked_user = UserFactory()
        mock_get_or_create_user.return_value = mocked_user
        mock_user_exists.return_value = True
        mock_encrypt_token.return_value = "encrypted_token"

        user, token = business.get_or_create_user({"sub": mocked_user.google_id})
        self.assertEqual(mocked_user.to_dict(), user.to_dict())
        self.assertEqual(token, "encrypted_token")

        # Make sure default columns not re-created
        mock_create_default_columns.assert_not_called()


@patch("account.query.update_user")
class UpdateUserTests(TestCase):
    def test_update_user_valid_birthday(self, mock_update_user):
        user = UserFactory()
        business.update_user(payload={"id": user.id, "birthday": "2023-02-12T16:31:00.000Z"})
        mock_update_user.assert_called_with({"id": user.id, "birthday": "2023-02-12"})

    def test_update_user_invalid_birthday(self, mock_update_user):
        user = UserFactory()
        with self.assertRaises(AttributeError):
            business.update_user(payload={"id": user.id, "birthday": "2023-02"})
        mock_update_user.assert_not_called()


class PrivacyTests(TestCase):
    @patch("account.query.create_privacies")
    def test_get_privacies(self, mock_create_privacies):
        mocked_priv = PrivacyFactory()
        mock_create_privacies.return_value = mocked_priv

        priv = business.get_privacies(mocked_priv.user.id)
        self.assertEqual(mocked_priv.to_dict(), priv.to_dict())

    @patch("account.query.update_privacies")
    def test_update_privacies(self, mock_update_privacies):
        mocked_priv = PrivacyFactory()
        newPrivDict = {
            "is_searchable": False,
            "share_kanban": True,
            "cover_letter_requestable": False,
        }
        # payload to `update` is *not* a Privacy dict, but a dict of values
        business.update_privacies({"user_id": mocked_priv.user.id, "privacies": newPrivDict})
        mock_update_privacies.assert_called_with(in_user_id=mocked_priv.user.id, payload=newPrivDict)

    @patch("account.query.update_privacies")
    def test_invalid_update_privacies(self, mock_update_privacies):
        mocked_priv = PrivacyFactory()
        # test updating with an attribute error
        mock_update_privacies.side_effect = AttributeError("Attribute not found.")
        badPrivDict = {
            "is_able": False,
            "share_kanban": True,
            "cover_letter_requestable": False,
        }
        with self.assertRaises(AttributeError):
            business.update_privacies({"user_id": mocked_priv.user.id, "privacies": badPrivDict})


class FriendTests(TestCase):
    @patch("account.query.add_friend")
    def test_invalid_add_friend(self, mock_add_friend):
        # The only thing the business layer does for this is verify that the users are different, so that's all we're
        # testing for here
        with self.assertRaises(ValueError):
            business.add_friend(0, 0)

        # The query layer handles verifying that the users exist, so here we only care that it calls the query function
        business.add_friend(0, 1)
        mock_add_friend.assert_called()

    @patch("account.query.remove_friend")
    def test_invalid_remove_friend(self, mock_remove_friend):
        # I guess there's nothing stopping a user from removing friends with themselves, since that method is defined
        # such that it doesn't doesn't do anything if the user(s) involved are already not friends
        business.remove_friend(0, 0)
        mock_remove_friend.assert_called()


@patch("account.query.get_user_by_token_fields")
@patch("account.business.decrypt_token")
class AuthenticateTokenTests(TestCase):
    @patch("account.business.encrypt_token")
    def test_authenticate_token_valid(self, mock_encrypt_token, mock_decrypt_token, mock_get_user_by_token_fields):
        user = UserFactory()
        mock_get_user_by_token_fields.return_value = user
        mock_encrypt_token.return_value = "new_token"
        mock_decrypt_token.return_value = {"google_id": "gid", "last_login": "2023-03-03 01:28:02.710196+00:00"}
        valid_token = "xyz"
        response = business.authenticate_token(valid_token)
        self.assertEqual(response, (user, "new_token"))

    def test_authenticate_token_invalid(self, mock_decrypt_token, mock_get_user_by_token_fields):
        mock_get_user_by_token_fields.side_effect = ObjectDoesNotExist("Invalid Get")
        mock_decrypt_token.return_value = {"google_id": "gid", "last_login": "2023-03-03 01:28:02.710196+00:00"}
        invalid_token = "xyz"
        with self.assertRaises(ObjectDoesNotExist):
            business.authenticate_token(invalid_token)


@patch("account.query.pending_friend_request_exists")
@patch("account.query.are_friends")
@patch("account.query.get_privacies")
@patch("account.query.create_friend_request")
class CreateFriendRequestTests(TestCase):
    def test_create_friend_request_valid(
        self, mock_create_friend_request, mock_get_privacies, mock_are_friends, mock_pending_friend_request_exists
    ):
        req = FriendRequestFactory()
        mock_create_friend_request.return_value = req
        mock_are_friends.return_value = False
        mock_get_privacies.return_value = PrivacyFactory(is_searchable=True)
        mock_pending_friend_request_exists.return_value = False

        self.assertEqual(business.create_friend_request(req.from_user.id, req.to_user.id).to_dict(), req.to_dict())

    def test_create_friend_pending_request_exists(
        self, mock_create_friend_request, mock_get_privacies, mock_are_friends, mock_pending_friend_request_exists
    ):
        req = FriendRequestFactory()
        mock_create_friend_request.return_value = req
        mock_are_friends.return_value = False
        mock_get_privacies.return_value = PrivacyFactory(is_searchable=True)
        mock_pending_friend_request_exists.return_value = True

        with self.assertRaises(ValueError):
            business.create_friend_request(req.from_user.id, req.to_user.id)

    def test_create_friend_request_already_friends(
        self, mock_create_friend_request, mock_get_privacies, mock_are_friends, mock_pending_friend_request_exists
    ):
        req = FriendRequestFactory()
        mock_create_friend_request.return_value = req
        mock_are_friends.return_value = True
        mock_get_privacies.return_value = PrivacyFactory(is_searchable=True)
        mock_pending_friend_request_exists.return_value = False

        with self.assertRaises(ValueError):
            business.create_friend_request(req.from_user.id, req.to_user.id)

    def test_create_friend_request_user_not_searchable(
        self, mock_create_friend_request, mock_get_privacies, mock_are_friends, mock_pending_friend_request_exists
    ):
        req = FriendRequestFactory()
        mock_create_friend_request.return_value = req
        mock_are_friends.return_value = False
        mock_get_privacies.return_value = PrivacyFactory(is_searchable=False)
        mock_pending_friend_request_exists.return_value = False

        with self.assertRaises(ValueError):
            business.create_friend_request(req.from_user.id, req.to_user.id)


@patch("account.query.pending_friend_request_exists")
@patch("account.query.accept_friend_request")
class AcceptFriendRequestTests(TestCase):
    def test_accept_friend_request_valid(self, mock_accept_friend_request, mock_pending_friend_request_exists):
        req = FriendRequestFactory()
        mock_pending_friend_request_exists.return_value = True

        business.accept_friend_request(request_id=req.id, user_id=req.to_user.id)
        mock_accept_friend_request.assert_called_with(request_id=req.id, to_user_id=req.to_user.id)

    def test_accept_friend_request_no_pending_request(
        self, mock_accept_friend_request, mock_pending_friend_request_exists
    ):
        req = FriendRequestFactory()
        mock_pending_friend_request_exists.return_value = False

        with self.assertRaises(ObjectDoesNotExist):
            business.accept_friend_request(request_id=req.id, user_id=req.to_user.id)
        mock_accept_friend_request.assert_not_called()


@patch("account.query.pending_friend_request_exists")
@patch("account.query.deny_friend_request")
class DenyFriendRequestTests(TestCase):
    def test_deny_friend_request_valid(self, mock_deny_friend_request, mock_pending_friend_request_exists):
        req = FriendRequestFactory()
        mock_pending_friend_request_exists.return_value = True

        business.deny_friend_request(request_id=req.id, user_id=req.to_user.id)
        mock_deny_friend_request.assert_called_with(request_id=req.id, to_user_id=req.to_user.id)

    def test_deny_friend_request_no_pending_request(self, mock_deny_friend_request, mock_pending_friend_request_exists):
        req = FriendRequestFactory()
        mock_pending_friend_request_exists.return_value = False

        with self.assertRaises(ObjectDoesNotExist):
            business.deny_friend_request(request_id=req.id, user_id=req.to_user.id)
        mock_deny_friend_request.assert_not_called()


@patch("account.query.get_friend_requests_status")
class GetFriendRequestsStatusTests(TestCase):
    def test_get_friend_requests_status(self, mock_get_friend_requests_status):
        return_val = [], []
        mock_get_friend_requests_status.return_value = return_val
        val = business.get_friend_requests_status(user_id=0)
        self.assertEqual(val, return_val)
