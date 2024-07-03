from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'started_at', 'finished_at', 'legit',
                            'player1_score', 'player2_score', 'winner')
