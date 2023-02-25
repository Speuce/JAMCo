from unittest import TestCase
from column.tests.factories import KanbanColumnFactory
from column.models import KanbanColumn


class FactoryTest(TestCase):
    def test_factory(self):
        KanbanColumnFactory()
        self.assertEqual(KanbanColumn.objects.count(), 1)
