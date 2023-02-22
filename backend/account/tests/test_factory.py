from unittest import TestCase
from account.tests.factories import UserFactory
from account.models import User


class FactoryTest(TestCase):
    def test_factory(self):
        UserFactory()
        self.assertEqual(User.objects.count(), 1)
