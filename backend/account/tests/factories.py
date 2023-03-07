from account.models import User
import factory
import factory.django


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker("localized_ean13")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "username%d" % n)
    email = factory.Faker("ascii_safe_email")
    google_id = factory.Faker("localized_ean13")
