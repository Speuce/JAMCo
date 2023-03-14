from django.test import TransactionTestCase
from account.tests.factories import UserFactory, PrivacyFactory, FriendRequestFactory
from account.models import User, Privacy, FriendRequest


class FactoryTest(TransactionTestCase):
    reset_sequences = True

    def test_user_factory(self):
        UserFactory()
        self.assertEqual(User.objects.count(), 1)

    def test_privacy_factory(self):
        PrivacyFactory()
        self.assertEqual(Privacy.objects.count(), 1)

    def test_friend_request_factory(self):
        FriendRequestFactory()
        self.assertEqual(FriendRequest.objects.count(), 1)
