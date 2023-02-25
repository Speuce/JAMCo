import datetime
from django.test import TestCase
from account import business
from column.business import get_columns


class CreateUserTests(TestCase):
    def test_create_user(self):
        # Make sure default columns are created
        user, created = business.get_or_create_user({"sub": "4"})
        columns = get_columns(user.id)
        self.assertEqual(columns[0].name, "To Apply")
        self.assertEqual(columns[1].name, "Application Submitted")
        self.assertEqual(columns[2].name, "OA")
        self.assertEqual(columns[3].name, "Interview")


class UpdateUserTests(TestCase):
    def test_update_user_valid_birthday(self):
        user, created = business.get_or_create_user({"sub": "4"})
        business.update_user(payload={"id": user.id, "birthday": "2023-02-12T16:31:00.000Z"})
        updated_user, created = business.get_or_create_user({"sub": "4"})
        self.assertEqual(updated_user.birthday, datetime.date(2023, 2, 12))

    def test_update_user_invalid_birthday(self):
        user, created = business.get_or_create_user({"sub": "5"})
        with self.assertRaises(AttributeError):
            business.update_user(payload={"id": user.id, "birthday": "2023-02"})


class FriendTests(TestCase):
    def test_invalid_add_friend(self):
        # The only thing the business layer does for this is verify that the users are different, so that's all we're
        # testing for here
        with self.assertRaises(ValueError):
            business.add_friend(0, 0)
