import time
import json

from .models import Game
from .pong_controller import PaddleController, GameState
from .thread_pool import ThreadPool
from backend.settings import logger


from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PongConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.thread = None
        self.game = None
        self.paddle_controller = None

        super().__init__(*args, **kwargs)

    def connect(self):

        try:
            self.game = Game.objects.get(id=self.scope['url_route']['kwargs']['game'])
        except Game.DoesNotExist:
            self.accept()
            self.send(text_data=json.dumps({
                'error': 'Game not found'
            }))
            self.close()
            return
        if self.scope['user'] != self.game.player1 and self.scope['user'] != self.game.player2:
            self.accept()
            self.send(text_data=json.dumps({
                'error': 'You are not a player of this game'
            }))
            self.close()
            return
        if self.game.finished_at:
            self.accept()
            self.send(text_data=json.dumps({
                'error': 'Game is already finished'
            }))
            self.close()
            return

        # If the game is not in the thread pool, add it and pass game object
        if str(self.game.pk) not in ThreadPool.threads:
            ThreadPool.add_game(self.game, self)

        self.thread = ThreadPool.threads[str(self.game.pk)]

        async_to_sync(self.channel_layer.group_add)(str(self.game.pk), self.channel_name)

        if self.scope['user'] == self.game.player1:
            if not self.thread["Game"].paddle_one:
                logger.warning("Creating paddle one for game " + str(self.game.pk))
                self.thread["Game"].paddle_one = PaddleController()
            self.paddle_controller = self.thread["Game"].paddle_one
            self.thread["active_connections"] += 1
        elif self.scope['user'] == self.game.player2:
            if not self.thread["Game"].paddle_two:
                logger.warning("Creating paddle two for game " + str(self.game.pk))
                self.thread["Game"].paddle_two = PaddleController()
            self.paddle_controller = self.thread["Game"].paddle_two
            self.thread["active_connections"] += 1

        if self.thread["active_connections"] == 2:
            self.thread["Game"].start_game()

        self.accept()

    def disconnect(self, close_code):
        if self.game:
            if self.thread["Game"].state != GameState.FINISHED:
                self.thread["Game"].state = GameState.PAUSED

            self.thread["active_connections"] -= 1
            self.thread[str(self.paddle_controller)] = False
            self.thread["active"] = False

            async_to_sync(self.channel_layer.group_discard)(str(self.game.pk), self.channel_name)

    def receive(self, text_data):
        if self.thread["Game"].state == GameState.PAUSED:
            return

        direction = json.loads(text_data).get("direction")
        self.paddle_controller.move(direction)

    def propagate_state(self):
        tick_rate = 1 / 64
        while True:
            start_time = time.time()

            if self.thread:
                if self.thread["Game"].state == GameState.IN_PROGRESS:
                    self.thread["Game"].ball.move()
                    self.thread["Game"].end_game()

                    async_to_sync(self.channel_layer.group_send)(
                        str(self.game.pk),
                        {"type": "stream_state", "state": self.thread["Game"].stream()},
                    )
                if self.thread["Game"].state == GameState.PAUSED:
                    async_to_sync(self.channel_layer.group_send)(
                        str(self.game.pk),
                        {"type": "game_paused", "state": self.thread["Game"].stream()},
                    )
                if self.thread["Game"].state == GameState.FINISHED:
                    async_to_sync(self.channel_layer.group_send)(
                        str(self.game.pk),
                        {"type": "game_finished"},
                    )
                    break

            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time < tick_rate:
                time.sleep(tick_rate - elapsed_time)

    def stream_state(self, event):
        self.send(text_data=json.dumps(event["state"]))

    def game_paused(self, event):
        self.send(text_data=json.dumps({**event["state"], "error": "Game is paused"}))

    def game_finished(self, event):
        self.close()
