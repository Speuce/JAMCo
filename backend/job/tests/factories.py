from job.models import Job
from column.tests.factories import KanbanColumnFactory
from account.tests.factories import UserFactory
import factory
import factory.django


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    kcolumn = factory.SubFactory(KanbanColumnFactory)
    user = factory.SubFactory(UserFactory)
    position_title = "Position"
    company = "Company"
