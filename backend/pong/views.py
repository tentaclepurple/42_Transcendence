from rest_framework import generics

from .models import Game
from .serializers import GameSerializer

# Create your views here.

class GameListCreateView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        serializer.save()
        ## TODO: Adding the requester to the request
        ##serializer.save(player1=self.request.user)

class GameRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

