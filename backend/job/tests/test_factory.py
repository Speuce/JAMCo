from unittest import TestCase
from job.tests.factories import JobFactory
from job.models import Job


class FactoryTest(TestCase):
    def test_factory(self):
        JobFactory()
        self.assertEqual(Job.objects.count(), 1)
