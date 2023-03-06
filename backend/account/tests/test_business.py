from django.test import TestCase
from account import business
from unittest.mock import patch
from account.tests.factories import UserFactory, PrivacyFactory


@patch("account.query.get_or_create_user")
@patch("account.query.user_exists")
@patch("account.business.create_default_columns")
class GetOrCreateUserTests(TestCase):
    def test_get_or_create_user_new(self, mock_create_default_columns, mock_user_exists, mock_get_or_create_user):
        mocked_user = UserFactory()
        mock_get_or_create_user.return_value = mocked_user
        mock_user_exists.return_value = False

        user, created = business.get_or_create_user({"sub": mocked_user.google_id})
        self.assertEqual(mocked_user.to_dict(), user.to_dict())
        self.assertTrue(created)

        # Make sure default columns are created
        mock_create_default_columns.assert_called_with(mocked_user.id)

    def test_get_or_create_user_existing(self, mock_create_default_columns, mock_user_exists, mock_get_or_create_user):
        mocked_user = UserFactory()
        mock_get_or_create_user.return_value = mocked_user
        mock_user_exists.return_value = True

        user, created = business.get_or_create_user({"sub": mocked_user.google_id})
        self.assertEqual(mocked_user.to_dict(), user.to_dict())
        self.assertFalse(created)

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
        business.update_privacies({"user": mocked_priv.user, "privacies": newPrivDict})
        mock_update_privacies.assert_called_with(user_id=mocked_priv.user.id, payload=newPrivDict)

    @patch("account.query.update_privacies")
    def test_invalid_update_privacies(self, mock_update_privacies):
        # test updating without one of the fields
        mocked_priv = PrivacyFactory()
        newPrivDict = {
            "is_searchable": False,
            "share_kanban": True,
            "cover_letter_requestable": False,
        }
        # payload to `update` is *not* a Privacy dict, but a dict of values
        with self.assertRaises(AttributeError):
            business.update_privacies({"privacies": newPrivDict})

        # test updating with an attribute error
        mock_update_privacies.side_effect = AttributeError("Attribute not found.")
        badPrivDict = {
            "is_able": False,
            "share_kanban": True,
            "cover_letter_requestable": False,
        }
        with self.assertRaises(AttributeError):
            business.update_privacies({"user": mocked_priv.user, "privacies": badPrivDict})


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
