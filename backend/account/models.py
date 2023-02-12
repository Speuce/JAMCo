from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Name, username, and email are included with AbstractUser
    google_id = models.TextField(unique=True)
    image_url = models.TextField(null=True)
    country = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    birthday = models.DateField(verbose_name="Date of Birth", null=True)
    field_of_work = models.CharField(max_length=30, null=True)

    def to_dict(self):
        return {
            "google_id": self.google_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "image_url": self.image_url,
            "country": self.country,
            "city": self.city,
            "birthday": self.birthday,
            "field_of_work": self.field_of_work,
            "last_login": self.last_login,
        }
