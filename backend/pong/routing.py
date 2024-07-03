from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("pong/<int:game>/", consumers.PongConsumer.as_asgi()),
]
