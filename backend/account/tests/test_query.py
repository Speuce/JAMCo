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
        self.assertEqual(
            query.get_or_create_user({
                "sub": "4"
            }).first_name, "Rob")

    def test_invalid_update_account(self):
        # Create an account first # 'sub' is the field name from google tokens
        user = query.get_or_create_user({"sub": "4"})

        # "Update" the user
        with self.assertRaises(AttributeError):
            query.update_user({"id": user.id, "favourite_prof": "Rasit"})

        # Update the "user"
        # User doesn't exist
        with self.assertRaises(ValueError):
            query.update_user({
                "id": "41 6D 6F 6E 67 20 55 73",
                "first_name": "Rob"
            })
        # User not specified
        with self.assertRaises(ObjectDoesNotExist):
            query.update_user({"first_name": "Rob"})


class CreateColumnTests(TestCase):

    def test_create_column(self):
        user = query.get_or_create_user({"sub": "4"})
        new_column = query.create_column(user.id, "New column", 0)
        newer_column = query.create_column(user.id, "Newer column", 1)

        # Column numbers should be in order of creation by default
        self.assertEqual(new_column.column_number, 0)
        self.assertEqual(newer_column.column_number, 1)

    def test_duplicate_column_names(self):
        user = query.get_or_create_user({"sub": "4"})
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newer column", 1)

        # Duplicate names are allowed
        duplicate_name_column = query.create_column(user.id, "Newer column", 2)
        self.assertEqual(duplicate_name_column.column_number, 2)

    def test_invalid_create_column(self):
        # User doesn't exist
        with self.assertRaises(ObjectDoesNotExist):
            query.create_column(-1, "New column", 0)


class GetColumnsTests(TestCase):

    def test_get_columns(self):
        user = query.get_or_create_user({"sub": "4"})
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newest column", 1)
        query.create_column(user.id, "Newester column", 2)
        # Make another user
        user2 = query.get_or_create_user({"sub": "5"})
        query.create_column(user2.id, "New column", 0)
        query.create_column(user2.id, "Newest column", 1)
        query.create_column(user2.id, "Newester column", 2)
        query.create_column(user2.id, "Newesterest column", 3)

        columns = query.get_columns(user.id)

        # The query should only return the columns for the specified user
        self.assertEqual(columns.count(), 3)
        for column in columns:
            self.assertEqual(column.user.id, user.id)


class DeleteColumnsTests(TestCase):

    def test_delete_column(self):
        user = query.get_or_create_user({"sub": "4"})
        column1 = query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newester column", 1)

        query.delete_column(user.id, 0)
        self.assertEqual(len(query.get_columns(user.id)), 1)

    def test_delete_columns(self):
        user = query.get_or_create_user({"sub": "4"})
        column1 = query.create_column(user.id, "New column", 0)
        column2 = query.create_column(user.id, "Newest column", 1)
        query.create_column(user.id, "Newester column", 2)
        # Make another user
        user2 = query.get_or_create_user({"sub": "5"})
        query.create_column(user2.id, "New column", 0)
        query.create_column(user2.id, "Newest column", 1)
        query.create_column(user2.id, "Newester column", 2)
        query.create_column(user2.id, "Newesterest column", 3)

        query.delete_columns([column1.id, column2.id])
        self.assertEqual(len(query.get_columns(user.id)), 1)
        self.assertEqual(len(query.get_columns(user2.id)), 4)

    def test_invalid_delete_columns(self):
        user = query.get_or_create_user({"sub": "4"})
        query.create_column(user.id, "New column", 0)
        query.create_column(user.id, "Newest column", 1)

        # Try deleting a column that doesn't exist
        # By the pigeonhole principle, one of these ids must be invalid ;)
        query.delete_columns([1, 2, 3])


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
