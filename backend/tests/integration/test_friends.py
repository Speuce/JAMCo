import json
from django.test import TransactionTestCase
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from account.tests.factories import UserFactory, PrivacyFactory, FriendRequestFactory
from account.models import FriendRequest, User


class CreateFriendRequestTests(TransactionTestCase):
    reset_sequences = True

    def test_create_friend_request_valid(self):
        user_one = UserFactory()
        PrivacyFactory(user=user_one)
        user_two = UserFactory()
        PrivacyFactory(user=user_two)

        response = self.client.post(
            reverse("create_friend_request"),
            json.dumps({"from_user_id": user_one.id, "to_user_id": user_two.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        self.assertEqual(content["from_user_id"], user_one.id)
        self.assertEqual(content["to_user_id"], user_two.id)
        self.assertEqual(content["accepted"], False)
        self.assertEqual(content["acknowledged"], None)
        self.assertTrue(datetime.strptime(content["sent"], "%Y-%m-%d %H:%M:%S.%f%z") < timezone.now())

    def test_create_friend_request_error(self):
        # to_user not searchable
        user_one = UserFactory()
        PrivacyFactory(user=user_one)
        user_two = UserFactory()
        PrivacyFactory(user=user_two, is_searchable=False)

        response = self.client.post(
            reverse("create_friend_request"),
            json.dumps({"from_user_id": user_one.id, "to_user_id": user_two.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(FriendRequest.objects.all()), 0)

        # already friends
        user_one = UserFactory()
        PrivacyFactory(user=user_one)
        user_two = UserFactory()
        PrivacyFactory(user=user_two)

        user_one.friends.add(user_two)

        response = self.client.post(
            reverse("create_friend_request"),
            json.dumps({"from_user_id": user_one.id, "to_user_id": user_two.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(FriendRequest.objects.all()), 0)

        # pending request exists
        user_one = UserFactory()
        PrivacyFactory(user=user_one)
        user_two = UserFactory()
        PrivacyFactory(user=user_two)

        FriendRequestFactory(from_user=user_one, to_user=user_two)
        self.assertEqual(len(FriendRequest.objects.all()), 1)

        response = self.client.post(
            reverse("create_friend_request"),
            json.dumps({"from_user_id": user_one.id, "to_user_id": user_two.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(FriendRequest.objects.all()), 1)


class AcceptFriendRequestTests(TransactionTestCase):
    reset_sequences = True

    def test_accept_friend_request_valid(self):
        req = FriendRequestFactory()
        PrivacyFactory(user=req.to_user)

        self.assertFalse(FriendRequest.objects.get(id=req.id).acknowledged)
        response = self.client.post(
            reverse("accept_friend_request"),
            json.dumps({"request_id": req.id, "to_user_id": req.to_user.id, "from_user_id": req.from_user.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(FriendRequest.objects.get(id=req.id).accepted)
        self.assertTrue(FriendRequest.objects.get(id=req.id).acknowledged)
        self.assertTrue(User.objects.get(id=req.from_user.id).friends.contains(req.to_user))
        self.assertTrue(User.objects.get(id=req.to_user.id).friends.contains(req.from_user))

    def test_accept_friend_request_error(self):
        req = FriendRequestFactory(acknowledged=timezone.now())
        PrivacyFactory(user=req.to_user)

        self.assertTrue(FriendRequest.objects.get(id=req.id))
        response = self.client.post(
            reverse("accept_friend_request"),
            json.dumps({"request_id": req.id, "to_user_id": req.to_user.id, "from_user_id": req.from_user.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.get(id=req.from_user.id).friends.contains(req.to_user))
        self.assertFalse(User.objects.get(id=req.to_user.id).friends.contains(req.from_user))


class DenyFriendRequestTests(TransactionTestCase):
    reset_sequences = True

    def test_deny_friend_request_valid(self):
        req = FriendRequestFactory()
        PrivacyFactory(user=req.to_user)

        self.assertFalse(FriendRequest.objects.get(id=req.id).acknowledged)
        response = self.client.post(
            reverse("deny_friend_request"),
            json.dumps({"request_id": req.id, "to_user_id": req.to_user.id, "from_user_id": req.from_user.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(FriendRequest.objects.get(id=req.id).accepted)
        self.assertTrue(FriendRequest.objects.get(id=req.id).acknowledged)
        self.assertFalse(User.objects.get(id=req.from_user.id).friends.contains(req.to_user))
        self.assertFalse(User.objects.get(id=req.to_user.id).friends.contains(req.from_user))

    def test_deny_friend_request_error(self):
        req = FriendRequestFactory()
        PrivacyFactory(user=req.to_user)
        alt_user = UserFactory()

        self.assertTrue(FriendRequest.objects.get(id=req.id))
        response = self.client.post(
            reverse("deny_friend_request"),
            json.dumps({"request_id": req.id, "user_id": alt_user.id, "from_user_id": req.from_user.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(FriendRequest.objects.get(id=req.id).accepted)
        self.assertFalse(FriendRequest.objects.get(id=req.id).acknowledged)
        self.assertFalse(User.objects.get(id=req.from_user.id).friends.contains(req.to_user))
        self.assertFalse(User.objects.get(id=req.to_user.id).friends.contains(req.from_user))


class GetFriendRequestsStatusTests(TransactionTestCase):
    reset_sequences = True

    def test_get_friend_requests_status_valid(self):
        user_one = UserFactory()
        PrivacyFactory(user=user_one)
        user_two = UserFactory()
        PrivacyFactory(user=user_two)

        # requests sent from user_one
        sent_one = FriendRequestFactory(from_user=user_one, to_user=user_two)
        sent_two = FriendRequestFactory(from_user=user_one, to_user=user_two)
        sent_three = FriendRequestFactory(from_user=user_one, to_user=user_two)
        sent_requests = [sent_one, sent_two, sent_three]

        # requests received by user_one
        received_one = FriendRequestFactory(to_user=user_one)
        received_two = FriendRequestFactory(to_user=user_one)
        received_requests = [received_one, received_two]

        response = self.client.post(
            reverse("get_friend_requests_status"),
            json.dumps({"user_id": user_one.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        sent = json.loads(response.content)["sent"]
        received = json.loads(response.content)["received"]

        for req in range(len(sent)):
            self.assertEqual(sent[req]["id"], sent_requests[req].id)
            self.assertEqual(sent[req]["from_user_id"], sent_requests[req].from_user.id)
            self.assertEqual(sent[req]["to_user_id"], sent_requests[req].to_user.id)
            self.assertEqual(sent[req]["acknowledged"], sent_requests[req].acknowledged)
            self.assertEqual(sent[req]["accepted"], sent_requests[req].accepted)

        for req in range(len(received)):
            self.assertEqual(received[req]["id"], received_requests[req].id)
            self.assertEqual(received[req]["from_user_id"], received_requests[req].from_user.id)
            self.assertEqual(received[req]["to_user_id"], received_requests[req].to_user.id)
            self.assertEqual(received[req]["acknowledged"], received_requests[req].acknowledged)
            self.assertEqual(received[req]["accepted"], received_requests[req].accepted)

    def test_get_friend_requests_status_error(self):
        response = self.client.post(
            reverse("get_friend_requests_status"),
            json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
