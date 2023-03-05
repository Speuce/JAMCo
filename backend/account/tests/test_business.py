from django.test import TestCase
from account import business
from unittest.mock import patch
from account.tests.factories import UserFactory
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
