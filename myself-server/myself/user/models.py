from django.db import models
from django.contrib.auth.models import AbstractUser
from store.models import *


class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to="users_img", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"


class Favorite(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Избранное для {self.user.username}"
