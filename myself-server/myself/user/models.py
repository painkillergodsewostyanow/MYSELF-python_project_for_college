from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to="users_img", null=True, blank=True)
