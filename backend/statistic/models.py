from django.db import models
from django.conf import settings
from users.models import MyUser as User

# Create your models here.

class Statistic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    elo = models.IntegerField(default=1200)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
