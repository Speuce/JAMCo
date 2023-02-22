from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from account import query, models
from account.tests.factories import UserFactory


class GetOrCreateUserTests(TestCase):
    def test_create_and_get_account(self):
        # 'sub' is the field name from google tokens
        query.get_or_create_user({"sub": "4"})
        # A user should exist after that query
        self.assertTrue(models.User.objects.filter(google_id="4").exists())

        # Repeating the query should result in retrieving the user, not creating
        # another one
        query.get_or_create_user({"sub": "4"})
        self.assertTrue(models.User.objects.filter(google_id="4").exists())
        self.assertEqual(models.User.objects.filter(google_id="4").count(), 1)


class UserExistsTests(TestCase):
    def test_user_exists(self):
        self.assertFalse(query.user_exists("4"))
        query.get_or_create_user({"sub": "4"})
        self.assertTrue(query.user_exists("4"))


class UpdateAccountTests(TestCase):
    def test_update_account(self):
        # Create an account first # 'sub' is the field name from google tokens
        user = UserFactory()

        # Update the user
        query.update_user({"id": user.id, "first_name": "Rob"})

        # The modifications should hold
        # Unable to properly mock this access without making test trivial
        self.assertEqual(query.get_or_create_user({"sub": user.google_id}).first_name, "Rob")

    def test_invalid_update_account(self):
        # Create an account first # 'sub' is the field name from google tokens
        user = UserFactory()

        # "Update" the user
        with self.assertRaises(AttributeError):
            query.update_user({"id": user.id, "favourite_prof": "Rasit"})

        # Update the "user"
        # User doesn't exist
        with self.assertRaises(ValueError):
            query.update_user({"id": "41 6D 6F 6E 67 20 55 73", "first_name": "Rob"})
        # User not specified
        with self.assertRaises(ObjectDoesNotExist):
            query.update_user({"first_name": "Rob"})
