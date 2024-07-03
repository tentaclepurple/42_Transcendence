from rest_framework import serializers
from .models import Tournament
from users.models import MyUser  # Asegúrate de importar el modelo MyUser si aún no lo has hecho

class TournamentSerializer(serializers.ModelSerializer):
    initiator = serializers.StringRelatedField()
    player1 = serializers.StringRelatedField()
    player2 = serializers.StringRelatedField()
    player3 = serializers.StringRelatedField()
    player4 = serializers.StringRelatedField()
    game1 = serializers.StringRelatedField()
    game2 = serializers.StringRelatedField()
    final_game = serializers.StringRelatedField()

    class Meta:
        model = Tournament
        fields = '__all__'
