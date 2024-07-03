from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, IntegerField
from statistic.user_statistic import update_elo_points

from typing import List
from users.models import MyUser
from .models import Game
from .serializers import GameSerializer
from backend.settings import logger

# Create your views here.

class GameRecordList(generics.ListCreateAPIView):
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            user = MyUser.objects.get(id=user_id)
        else:
            user = request.user
        games = Game.objects.filter(Q(player1=user) | Q(player2=user))
        return Response(GameSerializer.get_game_list(games))

class GameListCreateView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_elo_by_user(self, user: MyUser) -> List[int]:

        return Game.objects.filter(Q(player1=user) | Q(player2=user)).annotate(
            user_elo=Case(
                When(player1=user, then='player1_elo'),
                When(player2=user, then='player2_elo'),
                default=Value(0),  # default is optional, depends on your needs
                output_field=IntegerField()
            )
        )

    def get(self, request, *args, **kwargs):

        user_id = request.query_params.get("user", 0)
        
        if user_id:
            user = MyUser.objects.filter(id=int(user_id)).first()
        else:
            user = request.user

        games = self.get_elo_by_user(user)
        return Response(GameSerializer.get_games_json_list(games))


class GameRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_update(self, serializer):
        logger.warning("GameRetrieveUpdateView ----------->")
        serializer.save(user=self.request.user)


class GameListCreateViewSimulation(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):

        legit = serializer.validated_data.get("legit", False)

        if not legit:
            return

        winner = serializer.validated_data.get("winner", None)
        if winner is None:
            return
        
        player1 = serializer.validated_data.get("player1")
        player2 = serializer.validated_data.get("player2")

        if player1.id == winner:
            update_elo_points(player1.statistics, player2.statistics)
        else:
            update_elo_points(player2.statistics, player1.statistics)

        serializer.validated_data["player1_elo"] = player1.statistics.elo
        serializer.validated_data["player2_elo"] = player2.statistics.elo

        serializer.save()