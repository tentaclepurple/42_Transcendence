from django.db import models
from users.models import MyUser


# Create your models here.

class Game(models.Model):
    player1 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="player2")
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    winner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(default=None, null=True, blank=True)
    finished_at = models.DateTimeField(default=None, null=True, blank=True)
    legit = models.BooleanField(default=False)

    def __str__(self):
        return f"Game between {self.player1.username} and {self.player2.username}"


class Point(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    scored_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} scored at {self.scored_at}"

