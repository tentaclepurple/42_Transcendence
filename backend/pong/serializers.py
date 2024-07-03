from rest_framework import serializers
from .models import Game
from typing import List, Tuple, Dict, TypedDict
from datetime import datetime
from backend.settings import logger

class GameDict(TypedDict):
    player1: str
    player2: str
    player1_elo: int
    player2_elo: int
    created_at: datetime

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'started_at',
                            'player1_score', 'player2_score')

    @staticmethod
    def get_games_json_list(games: List[Game]) -> Tuple[List[int], List[datetime]]:
        elo_list = []
        finished_at_list = []
        for game in games:
            try:
                if game.user_elo == 0:
                    continue 

                elo_list.append(game.user_elo)
                finished_at_list.append(game.finished_at.strftime('%m-%d %H'))
            except Exception as ex:
                logger.warning(ex)
        return [elo_list, finished_at_list]

    @staticmethod
    def get_game_list(games: List[Game]) -> List[GameDict]:

        game_list = []

        for game in games:
            try:
                game_list.append({
                    "player1": game.player1.username,
                    "player2": game.player2.username,
                    "score1": game.player1_score,
                    "score2": game.player2_score,
                    "date": game.finished_at.strftime('%Y-%m-%d %H:%M')
                })
            except Exception as ex:
                logger.error(ex)
        return game_list