from django.urls import path
from .views import GameListCreateView, GameRetrieveUpdateView

urlpatterns = [
    path('games/', GameListCreateView.as_view()),
    path('games/<int:pk>/', GameRetrieveUpdateView.as_view())
]
