import factory
import factory.django
from account.tests.factories import UserFactory
from column.models import KanbanColumn


class KanbanColumnFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KanbanColumn

    user = factory.SubFactory(UserFactory)
    name = "Column Name"
    column_number = 1
