from job.models import Job
from column.tests.factories import KanbanColumnFactory
from account.tests.factories import UserFactory
import factory
import factory.django


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    id = factory.Faker("localized_ean8")
    kcolumn = factory.SubFactory(KanbanColumnFactory)
    user = factory.SubFactory(UserFactory)
    position_title = "Position"
    company = "Company"
    description = None
    notes = None
    cover_letter = None
    deadlines = None
    type = None
