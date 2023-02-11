from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Name, username, and email are included with AbstractUser
    google_id = models.TextField(unique=True)
    image_url = models.TextField()
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    birthday = models.DateField(verbose_name='Date of Birth')
    field_of_work = models.CharField(max_length=30)
