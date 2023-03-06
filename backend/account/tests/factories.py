from account.models import User, Privacy
import factory
import factory.django


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker("localized_ean8")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("domain_word")
    email = factory.Faker("ascii_safe_email")
    google_id = factory.Faker("localized_ean8")


class PrivacyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Privacy

    id = factory.Faker("localized_ean8")
    user = factory.SubFactory(UserFactory)
    is_searchable = True
    share_kanban = True
    cover_letter_requestable = True
