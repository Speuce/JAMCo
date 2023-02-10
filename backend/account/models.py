from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Name, username, and email are included with AbstractUser
    google_id = models.TextField()
    image_url = models.TextField()
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    birthday = models.DateField(verbose_name='Date of Birth')
    field_of_work = models.CharField(max_length=30)


class KanbanColumn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    column_number = models.IntegerField()

    def to_dict(self):
        return {'name': self.name, 'column_number': self.column_number}
