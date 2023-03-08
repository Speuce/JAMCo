from django.apps import AppConfig
from django.conf import settings


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        from .models import User

        if settings.IS_TEST:
            User.objects.filter(google_id="1234567890").delete()
