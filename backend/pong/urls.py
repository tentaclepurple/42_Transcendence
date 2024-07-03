from django.urls import path
from .views import GameListCreateView, GameListCreateViewSimulation, GameRetrieveUpdateView, GameRecordList

urlpatterns = [
    path('games/', GameListCreateView.as_view()),
    path('games/simulate/', GameListCreateViewSimulation.as_view()),
    path('games/<int:pk>/', GameRetrieveUpdateView.as_view()),
    path('games/me/', GameRecordList.as_view())
]
