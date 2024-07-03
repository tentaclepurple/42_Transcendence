from django.urls import path
from .views import TournamentDetails, TournamentCreate, CurrentTournaments, CreateFinal, MyTournaments

urlpatterns = [
    path('detail/<int:tournament_id>/', TournamentDetails.as_view(), name='tournament_detail'),
    path('create/', TournamentCreate.as_view(), name='tournament_create'),
    path('current/', CurrentTournaments.as_view(), name='current_tournaments'),

    path('create_final/', CreateFinal.as_view(), name='create_final'),
    path('my_tournaments/', MyTournaments.as_view(), name='my_tournament'),
]
