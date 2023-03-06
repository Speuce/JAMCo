from unittest import TestCase
from account.tests.factories import UserFactory, PrivacyFactory
from account.models import User, Privacy


class FactoryTest(TestCase):
    def test_factory(self):
        UserFactory()
        self.assertEqual(User.objects.count(), 1)

    def test_priv_factory(self):
        PrivacyFactory()
        self.assertEqual(Privacy.objects.count(), 1)
