from account.models import User, Privacy, FriendRequest
import factory
import factory.django
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "username%d" % n)
    email = factory.Faker("ascii_safe_email")
    google_id = factory.Faker("localized_ean13")


class PrivacyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Privacy

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    is_searchable = True
    share_kanban = True
    cover_letter_requestable = True


class FriendRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FriendRequest

    id = factory.Sequence(lambda n: n)
    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    sent = timezone.now()
    accepted = False
    acknowledged = None
