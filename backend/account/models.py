from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Name, username, and email are included with AbstractUser
    google_id = models.TextField()
    image_url = models.TextField()
    #location = models. todo: Import django-cities
    birthday = models.DateField(verbose_name='Date of Birth')
    field_of_work = models.CharField(max_length=30)
