from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    is_connected = models.BooleanField(default=False)
    is_42 = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpg')
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    blocked_users = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='blocked_by')
    chat_invitation = models.IntegerField(default=0)
    nickname = models.CharField(max_length=10, unique=True)

    REQUIRED_FIELDS = ['email', 'nickname']