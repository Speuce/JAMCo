from job.models import Job, ReviewRequest, Review
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


class ReviewRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReviewRequest

    id = factory.Sequence(lambda n: n)
    job = factory.SubFactory(JobFactory)
    reviewer = factory.SubFactory(UserFactory)
    message = "review plz 🥺👉👈"
    fulfilled = False


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    id = factory.Sequence(lambda n: n)
    request = factory.SubFactory(ReviewRequestFactory)
    response = "best cover letter I've ever seen 10/10"
    completed = None
