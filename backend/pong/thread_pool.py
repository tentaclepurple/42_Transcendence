import threading
from .pong_controller import GameController


class ThreadPool:

    threads = {}

    @classmethod
    def add_game(cls, game, consumer_instance):
        cls.threads[str(game.pk)] = {
            "thread": threading.Thread(target=consumer_instance.propagate_state),
            "active_connections": 0,
            "Game": GameController(game=game),
        }
        thread = cls.threads[str(game.pk)]["thread"]
        thread.daemon = True
        thread.start()
