# twofa/models.py

from django.db import models
from django.conf import settings
from users.models import MyUser

class TwoFaCode(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    code = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}: {self.code}"
