from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


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
            "friends": list(self.friends.values("id", "first_name", "last_name", "country")),
            "sent_friend_requests": list(
                self.request_sender.filter(acknowledged=None).values_list("to_user_id", flat=True)
            ),
            "received_friend_requests": list(
                self.request_receiver.filter(acknowledged=None).values(
                    "id", "from_user_id", "from_user__first_name", "from_user__last_name", "from_user__country"
                )
            ),
        }


class Privacy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_searchable = models.BooleanField(null=False)
    share_kanban = models.BooleanField(null=False)
    cover_letter_requestable = models.BooleanField(null=False)

    def to_dict(self):
        return {
            "id": self.id,
            "is_searchable": self.is_searchable,
            "share_kanban": self.share_kanban,
            "cover_letter_requestable": self.cover_letter_requestable,
        }


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="request_sender")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="request_receiver")
    sent = models.DateTimeField(verbose_name="Timestamp when request sent", null=False)
    accepted = models.BooleanField(default=False, null=False)
    acknowledged = models.DateTimeField(null=True, default=None)

    def to_dict(self):
        return {
            "from_user_id": self.from_user.id,
            "to_user_id": self.to_user.id,
            "sent": datetime.strftime(self.sent, "%Y-%m-%d %H:%M:%S.%f%z"),
            "accepted": self.accepted,
            "acknowledged": self.acknowledged,
        }
