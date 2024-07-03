import time
import random
from enum import Enum

from . import constants

from tournament.models import Tournament
from pong.models import Game
from .models import Point
from datetime import datetime
from backend.settings import logger
from statistic.user_statistic import update_elo_points
from blchain.views import blchain


class GameState(Enum):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    PAUSED = 3
    FINISHED = 4

def handle_tournament_game(game: Game) -> None:
    tournament = Tournament.objects.get(id=game.tournament_id)

    logger.warning(tournament)
    if tournament is None:
        logger.error(f"No tournament foudn with id: {game.tournament_id}")
        return

    if tournament.final_game:
        logger.warning(f"tournament finished, the winner is: {game.winner.nickname}" )
        tournament.end_time = datetime.now()
        tournament.save()
        payload = f"tournament_id={tournament.id} end={tournament.end_time} winner={tournament.final_game.winner.username}"
        blchain(payload)

    if tournament.game1.winner and tournament.game2.winner:
        logger.warning("Semifinals finished")
        tournament.final_game = Game.objects.create(
            player1=tournament.game1.winner,
            player2=tournament.game2.winner,
            tournament_id=tournament.id
        )
        tournament.save()

class GameController:

    def __init__(self, game):
        self.Game = game
        self.state = GameState.NOT_STARTED
        self.paddle_one = PaddleController()
        self.paddle_two = PaddleController()
        self.ball = BallController(self.Game, self.paddle_one, self.paddle_two)

    def start_game(self):
        self.paddle_two.x = constants.SCREEN_WIDTH - constants.PADDLE_WIDTH
        if not self.ball:
            self.ball = BallController(self.Game, self.paddle_one, self.paddle_two)
        self.state = GameState.IN_PROGRESS

    # Check if the game has to end
    def end_game(self):

        if self.paddle_one.score == constants.MAX_SCORE:
            self.Game.player1_score = self.paddle_one.score
            self.Game.player2_score = self.paddle_two.score
            self.Game.winner = self.Game.player1
            self.Game.finished_at = datetime.now()
            update_elo_points(self.Game.player1.statistics, self.Game.player2.statistics)
            self.Game.player1_elo = self.Game.player1.statistics.elo
            self.Game.player2_elo = self.Game.player2.statistics.elo
            self.Game.save()
            self.state = GameState.FINISHED
            if self.Game.tournament_id:
                handle_tournament_game(self.Game)
            return True

        if self.paddle_two.score == constants.MAX_SCORE:
            self.Game.player1_score = self.paddle_one.score
            self.Game.player2_score = self.paddle_two.score
            self.Game.winner = self.Game.player2
            self.Game.finished_at = datetime.now()
            update_elo_points(self.Game.player2.statistics, self.Game.player1.statistics)
            self.Game.player1_elo = self.Game.player1.statistics.elo
            self.Game.player2_elo = self.Game.player2.statistics.elo
            self.Game.save()
            self.state = GameState.FINISHED
            if self.Game.tournament_id:
                handle_tournament_game(self.Game)
            return True

        return False

    def stream(self):
        return {
            "game_state": self.state.name,
            "paddle_one": self.paddle_one.stream(),
            "paddle_two": self.paddle_two.stream(),
            "ball": self.ball.stream(),
        }


class PaddleController:
    def __init__(self):
        self.x = 0
        self.y = 225
        self.score = 0

    def move(self, direction):
        if direction == "down" and self.y < constants.MAX_PADDLE_Y:
            self.y += 5

        elif direction == "up" and self.y > 0:
            self.y -= 5

    def stream(self):
        return {
            "x": self.x,
            "y": self.y,
            "score": self.score,
        }


class BallController:
    def __init__(self, game, paddle_one, paddle_two):
        self.game = game
        self.game.started_at = datetime.now()
        self.game.save()

        self.x = 0
        self.y = 0
        self.paddle_one = paddle_one
        self.paddle_two = paddle_two

        self.reset_ball()

        self.time = time.time()

    def reset_ball(self):
        self.vel_x = random.choice([-2, 2])
        self.vel_y = 2
        self.x = constants.SCREEN_CENTER[0]
        self.y = 10

    def move(self):
        if time.time() - self.time > 0.01:
            if (
                    self.y > constants.MAX_BALL_Y
                    or self.y < constants.BALL_HEIGHT
            ):
                self.vel_y = -self.vel_y

            if 0 < self.x <= constants.PADDLE_WIDTH:
                if (
                        self.paddle_one.y
                        < self.y
                        < (self.paddle_one.y + constants.PADDLE_HEIGHT)
                ):
                    self.vel_x = -self.vel_x
                    self.x += 7

            elif self.x < 0:
                # Point is created in the database
                Point.objects.create(game=self.game, player=self.game.player2, x=self.x, y=self.y)
                self.paddle_two.score += 1
                self.reset_ball()

            elif constants.SCREEN_WIDTH > self.x >= constants.MAX_BALL_X:
                if (
                        self.paddle_two.y
                        < self.y
                        < (self.paddle_two.y + constants.PADDLE_HEIGHT)
                ):
                    self.vel_x = -self.vel_x
                    self.x -= 7

            elif self.x >= constants.SCREEN_WIDTH:
                # Point is created in the database
                Point.objects.create(game=self.game, player=self.game.player1, x=self.x, y=self.y)
                self.paddle_one.score += 1
                self.reset_ball()

            self.x += self.vel_x
            self.y += self.vel_y

            self.time = time.time()

    def stream(self):
        return {
            "x": self.x,
            "y": self.y,
        }
