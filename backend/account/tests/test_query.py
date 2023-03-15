from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from account import query, models
from account.tests.factories import UserFactory, PrivacyFactory, FriendRequestFactory
from django.utils import timezone
from datetime import datetime


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
        self.assertEqual(models.User.objects.get(id=user.id).first_name, "Rob")

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


class PrivacyTests(TestCase):
    def test_create_privacies(self):
        user = UserFactory()
        query.create_privacies(user.id)
        self.assertEqual(models.Privacy.objects.count(), 1)

    def test_get_privacies(self):
        priv = PrivacyFactory()
        user = priv.user
        privFetch = query.get_privacies(user.id)
        self.assertEqual(priv.id, privFetch.id)

    def test_invalid_privacies_get(self):
        priv = PrivacyFactory()
        user = priv.user
        self.assertEqual(models.Privacy.objects.count(), 1)
        # test invalid getting
        with self.assertRaises(ObjectDoesNotExist):
            query.get_privacies(user.id + 1)


class UpdatePrivacyTests(TestCase):
    def test_update_privacies(self):
        priv = PrivacyFactory()
        user = priv.user
        # update privacies to opposite of default
        query.update_privacies(
            user.id,
            {
                "is_searchable": False,
                "share_kanban": False,
                "cover_letter_requestable": False,
            },
        )
        newPriv = models.Privacy.objects.get(user__id=user.id)

        # verify updates succeeded
        self.assertDictEqual(
            newPriv.to_dict(),
            {
                "id": priv.id,
                "is_searchable": False,
                "share_kanban": False,
                "cover_letter_requestable": False,
            },
        )
        self.assertNotEqual(priv.to_dict(), newPriv.to_dict())

    def test_invalid_update_privacies(self):
        priv = PrivacyFactory()
        user = priv.user
        # update privacies to opposite of default
        with self.assertRaises(AttributeError):
            query.update_privacies(
                user.id,
                {
                    # invalid name
                    "searchable": False,
                    "share_kanban": False,
                    "cover_letter_requestable": False,
                },
            )

        newPriv = models.Privacy.objects.get(user__id=user.id)

        # verify updates succeeded
        self.assertDictEqual(
            newPriv.to_dict(),
            {
                "id": priv.id,
                "is_searchable": True,
                "share_kanban": True,
                "cover_letter_requestable": True,
            },
        )
        self.assertEqual(priv.to_dict(), newPriv.to_dict())


class FriendTests(TestCase):
    def test_add_friend(self):
        user1 = UserFactory()
        user2 = UserFactory()

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
        user = UserFactory()

        # Test user 1 not existing, user 2 not existing, and both users not existing
        with self.assertRaises(ObjectDoesNotExist):
            query.add_friend(-1, user.id)
        with self.assertRaises(ObjectDoesNotExist):
            query.add_friend(user.id, -1)
        with self.assertRaises(ObjectDoesNotExist):
            query.add_friend(-1, -1)

    def test_remove_friend(self):
        user1 = UserFactory()
        user2 = UserFactory()

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
        user = UserFactory()

        # Test user 1 not existing, user 2 not existing, and both users not existing
        with self.assertRaises(ObjectDoesNotExist):
            query.remove_friend(-1, user.id)
        with self.assertRaises(ObjectDoesNotExist):
            query.remove_friend(user.id, -1)
        with self.assertRaises(ObjectDoesNotExist):
            query.remove_friend(-1, -1)


class GetUserByTokenFieldsTests(TestCase):
    def test_get_user_by_token_fields(self):
        login = timezone.now()
        user = UserFactory(google_id="gID", last_login=login)
        retrieved_user = query.get_user_by_token_fields(user.google_id, login)
        self.assertEqual(user, retrieved_user)


class UpdateLastUserLoginTest(TestCase):
    def test_update_last_user_login(self):
        prev_login = datetime.strptime("2023-03-03 01:28:02.710196+00:00", "%Y-%m-%d %H:%M:%S.%f%z")
        user = UserFactory(last_login=prev_login)
        self.assertEqual(user.last_login, prev_login)
        query.update_user_last_login(user)
        self.assertNotEqual(user.last_login, prev_login)
        self.assertTrue(user.last_login > prev_login)


class CreateFriendRequestTest(TestCase):
    def test_create_friend_request(self):
        user_one = UserFactory()
        user_two = UserFactory()
        req = query.create_friend_request(from_user_id=user_one.id, to_user_id=user_two.id)
        self.assertEqual(models.FriendRequest.objects.count(), 1)
        self.assertEqual(models.FriendRequest.objects.get(id=req.id).to_dict(), req.to_dict())


class AcceptFriendRequestTest(TestCase):
    def test_accept_friend_request(self):
        req = FriendRequestFactory()
        self.assertEqual(models.FriendRequest.objects.count(), 1)
        self.assertFalse(req.acknowledged)

        query.accept_friend_request(request_id=req.id, to_user_id=req.to_user.id, from_user_id=req.from_user.id)
        self.assertEqual(models.FriendRequest.objects.count(), 1)

        updated_req = models.FriendRequest.objects.get(id=req.id)
        self.assertEqual(updated_req.accepted, True)
        self.assertTrue(updated_req.acknowledged)


class DenyFriendRequestTest(TestCase):
    def test_deny_friend_request(self):
        req = FriendRequestFactory()
        self.assertEqual(models.FriendRequest.objects.count(), 1)
        self.assertFalse(req.acknowledged)

        query.deny_friend_request(request_id=req.id, to_user_id=req.to_user.id, from_user_id=req.from_user.id)
        self.assertEqual(models.FriendRequest.objects.count(), 1)

        updated_req = models.FriendRequest.objects.get(id=req.id)
        self.assertEqual(updated_req.accepted, False)
        self.assertTrue(updated_req.acknowledged)


class GetFriendRequestsStatusTest(TestCase):
    def test_get_friend_requests_status_empty(self):
        user = UserFactory()
        sent, received = query.get_friend_requests_status(user.id)
        self.assertEqual(len(sent), 0)
        self.assertEqual(len(received), 0)

    def test_get_friend_requests_status_sent_none(self):
        req = FriendRequestFactory()
        sent, received = query.get_friend_requests_status(req.to_user.id)
        self.assertEqual(len(sent), 0)
        self.assertEqual(len(received), 1)

    def test_get_friend_requests_status_received_none(self):
        req = FriendRequestFactory()
        sent, received = query.get_friend_requests_status(req.from_user.id)
        self.assertEqual(len(sent), 1)
        self.assertEqual(len(received), 0)

    def test_get_friend_requests_status_populated(self):
        req_one = FriendRequestFactory()
        FriendRequestFactory(from_user=req_one.to_user)
        sent, received = query.get_friend_requests_status(req_one.to_user.id)
        self.assertEqual(len(sent), 1)
        self.assertEqual(len(received), 1)


class PendingFriendRequestExistsTest(TestCase):
    def test_pending_friend_request_exists_true_request_id(self):
        req = FriendRequestFactory()
        self.assertTrue(
            query.pending_friend_request_exists(
                request_id=req.id, to_user_id=req.to_user.id, from_user_id=req.from_user.id
            )
        )

    def test_pending_friend_request_exists_false_request_id(self):
        req = FriendRequestFactory(acknowledged=timezone.now())
        self.assertFalse(
            query.pending_friend_request_exists(
                request_id=req.id, to_user_id=req.to_user.id, from_user_id=req.from_user.id
            )
        )

    def test_pending_friend_request_exists_true_user_pair(self):
        req = FriendRequestFactory()
        self.assertTrue(query.pending_friend_request_exists(to_user_id=req.to_user.id, from_user_id=req.from_user.id))

    def test_pending_friend_request_exists_false_user_pair(self):
        req = FriendRequestFactory(acknowledged=timezone.now())
        self.assertFalse(query.pending_friend_request_exists(to_user_id=req.to_user.id, from_user_id=req.from_user.id))


class AreFriendsTest(TestCase):
    def test_are_friends_true(self):
        user_one = UserFactory()
        user_two = UserFactory()
        user_one.friends.add(user_two)
        user_two.friends.add(user_one)
        self.assertTrue(query.are_friends(user_one.id, user_two.id))
        self.assertTrue(query.are_friends(user_two.id, user_one.id))

    def test_are_friends_false(self):
        user_one = UserFactory()
        user_two = UserFactory()
        self.assertFalse(query.are_friends(user_one.id, user_two.id))
        self.assertFalse(query.are_friends(user_two.id, user_one.id))
