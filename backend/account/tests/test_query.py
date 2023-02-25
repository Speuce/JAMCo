from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from account import query, models


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
        user = query.get_or_create_user({"sub": "4"})

        # Update the user
        query.update_user({"id": user.id, "first_name": "Rob"})

        # The modifications should hold
        self.assertEqual(query.get_or_create_user({"sub": "4"}).first_name, "Rob")

    def test_invalid_update_account(self):
        # Create an account first # 'sub' is the field name from google tokens
        user = query.get_or_create_user({"sub": "4"})

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


class FriendTests(TestCase):
    def test_add_friend(self):
        user1 = query.get_or_create_user({"sub": "4"})
        user2 = query.get_or_create_user({"sub": "4"})

        query.add_friend(user1.id, user2.id)

        # They're friends now :)
        self.assertIn(user1, user2.friends.all())
        self.assertIn(user2, user1.friends.all())

        # Calling it again doesn't create more friendships
        user1_num_friends = user1.friends.count()
        user2_num_friends = user2.friends.count()
        query.add_friend(user1.id, user2.id)
        self.assertIn(user1, user2.friends.all())
        self.assertIn(user2, user1.friends.all())
        self.assertEqual(user1.friends.count(), user1_num_friends)
        self.assertEqual(user2.friends.count(), user2_num_friends)

    def test_invalid_add_friend(self):
        user = query.get_or_create_user({"sub": "4"})

        # Test user 1 not existing, user 2 not existing, and both users not existing
        with self.assertRaises(ObjectDoesNotExist):
            query.add_friend(-1, user.id)
        with self.assertRaises(ObjectDoesNotExist):
            query.add_friend(user.id, -1)
        with self.assertRaises(ObjectDoesNotExist):
            query.add_friend(-1, -1)

    def test_remove_friend(self):
        user1 = query.get_or_create_user({"sub": "4"})
        user2 = query.get_or_create_user({"sub": "4"})

        query.add_friend(user1.id, user2.id)
        # Make sure they were friends beforehand
        self.assertIn(user1, user2.friends.all())
        self.assertIn(user2, user1.friends.all())
        user1_num_friends = user1.friends.count()
        user2_num_friends = user2.friends.count()

        query.remove_friend(user1.id, user2.id)
        # :(
        self.assertNotIn(user1, user2.friends.all())
        self.assertNotIn(user2, user1.friends.all())
        self.assertEqual(user1.friends.count(), user1_num_friends - 1)
        self.assertEqual(user2.friends.count(), user2_num_friends - 1)

        # Calling it again doesn't remove more friendships
        user1_num_friends = user1.friends.count()
        user2_num_friends = user2.friends.count()
        query.remove_friend(user1.id, user2.id)
        self.assertNotIn(user1, user2.friends.all())
        self.assertNotIn(user2, user1.friends.all())
        self.assertEqual(user1.friends.count(), user1_num_friends)
        self.assertEqual(user2.friends.count(), user2_num_friends)

    def test_invalid_remove_friend(self):
        user = query.get_or_create_user({"sub": "4"})

        # Test user 1 not existing, user 2 not existing, and both users not existing
        with self.assertRaises(ObjectDoesNotExist):
            query.remove_friend(-1, user.id)
        with self.assertRaises(ObjectDoesNotExist):
            query.remove_friend(user.id, -1)
        with self.assertRaises(ObjectDoesNotExist):
            query.remove_friend(-1, -1)
