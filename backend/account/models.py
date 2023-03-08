from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Name, username, and email are included with AbstractUser
    google_id = models.TextField(unique=True)
    image_url = models.TextField(null=True)
    country = models.CharField(max_length=30, null=True)
    region = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    birthday = models.DateField(verbose_name="Date of Birth", null=True)
    field_of_work = models.CharField(max_length=30, null=True)
    friends = models.ManyToManyField("self")

    def to_dict(self):
        return {
            "id": self.id,
            "google_id": self.google_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "image_url": self.image_url,
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "birthday": self.birthday,
            "field_of_work": self.field_of_work,
        }


class Privacy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_searchable = models.BooleanField()
    share_kanban = models.BooleanField()
    cover_letter_requestable = models.BooleanField()

    def to_dict(self):
        return {
            "id": self.id,
            "is_searchable": self.is_searchable,
            "share_kanban": self.share_kanban,
            "cover_letter_requestable": self.cover_letter_requestable,
        }
