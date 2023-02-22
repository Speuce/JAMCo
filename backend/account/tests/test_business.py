from django.test import TestCase
from account import business
from unittest.mock import patch
from account.tests.factories import UserFactory


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
