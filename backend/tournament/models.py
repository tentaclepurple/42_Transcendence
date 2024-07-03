from django.db import models
from users.models import MyUser
from pong.models import Game

class Tournament(models.Model):
    initiator = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tournament_initiator')
    player1 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tournament_player1')
    player2 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tournament_player2')
    player3 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tournament_player3')
    player4 = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='tournament_player4')
    game1 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tournament_game1', null=True, blank=True)
    game2 = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tournament_game2', null=True, blank=True)
    final_game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tournament_final_game', null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Tournament initiated by {self.initiator.username} at {self.start_time}"

    def save(self, *args, **kwargs):
            if not self.player1:
                self.player1 = self.initiator
            super().save(*args, **kwargs)