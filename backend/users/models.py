from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    is_connected = models.BooleanField(default=False)
    is_42 = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

