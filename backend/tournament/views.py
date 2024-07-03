import random
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TournamentSerializer
from .models import Tournament
from pong.models import Game
from django.http import JsonResponse
from users.models import MyUser
from rest_framework import status
from django.db.models import Q
from pong.serializers import GameSerializer




class TournamentDetails(APIView):
    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, id=tournament_id)

        tournament_data = {
            'id': tournament.id,
            'initiator': tournament.initiator.username,
            'player1': tournament.player1.username,
            'player2': tournament.player2.username,
            'player3': tournament.player3.username,
            'player4': tournament.player4.username,
            'game1_id': tournament.game1.id if tournament.game1 else None,
            'game2_id': tournament.game2.id if tournament.game2 else None,
            'final_game_id': tournament.final_game.id if tournament.final_game else None,
            'game1_winner': tournament.game1.winner.username if tournament.game1 and tournament.game1.winner else None,
            'game2_winner': tournament.game2.winner.username if tournament.game2 and tournament.game2.winner else None,
            'final_game_winner': tournament.final_game.winner.username if tournament.final_game and tournament.final_game.winner else None,
            'start_time': tournament.start_time,
            'end_time': tournament.end_time,
        }

        return Response(tournament_data, status=status.HTTP_200_OK)


class TournamentCreate(APIView):
    def post(self, request):
        initiator = request.user 

        if not initiator.is_connected:
            return JsonResponse({'error': 'Initiator is not connected'}, status=400)

        connected_users = MyUser.objects.filter(is_connected=True).exclude(id=initiator.id)
        if len(connected_users) < 3:
            return JsonResponse({'error': 'Not enough connected users to create tournament'}, status=400)

        selected_users = random.sample(list(connected_users), 3)

        tournament = Tournament.objects.create(
            initiator = initiator,
            player1 = initiator,
            player2 = selected_users[0],
            player3 = selected_users[1],
            player4 = selected_users[2],
            start_time=datetime.now()
        )

        try:
            # Primera partida
            game1 = Game.objects.create(
                player1=tournament.player1,
                player2=tournament.player2,
                tournament_id=tournament.id
            )

            tournament.game1 = game1
            tournament.save()

            # Segunda partida
            game2 = Game.objects.create(
                player1=tournament.player3,
                player2=tournament.player4,
                tournament_id=tournament.id
            )

            tournament.game2 = game2
            tournament.save()

            # Serializar el objeto tournament y devolverlo en la respuesta
            serialized_tournament = {
                'id': tournament.id,
                'initiator': tournament.initiator.username,
                'player1': tournament.player1.username,
                'player2': tournament.player2.username,
                'player3': tournament.player3.username,
                'player4': tournament.player4.username if tournament.player4 else None,
                'game1': game1.id,
                'game2': game2.id,
                'start_time': tournament.start_time,
                # Añadir más campos según sea necesario
            }

            return JsonResponse(serialized_tournament, status=200)

        except Exception as e:
            # Manejar cualquier error que ocurra durante la creación de las partidas
            tournament.delete()  # Eliminar el torneo si ocurre algún error para evitar inconsistencias
            return JsonResponse({'error': str(e)}, status=500)



class CurrentTournaments(APIView):
    def get(self, request):
        current_tournaments = Tournament.objects.filter(start_time__isnull=False, end_time__isnull=True)
        tournaments_data = []

        for tournament in current_tournaments:
            tournament_data = {
                'id': tournament.id,
                'player1': tournament.player1.username,
                'player2': tournament.player2.username,
                'player3': tournament.player3.username,
                'player4': tournament.player4.username,
                'game1_winner': tournament.game1.winner.username if tournament.game1 and tournament.game1.winner else None,
                'game2_winner': tournament.game2.winner.username if tournament.game2 and tournament.game2.winner else None,
                'final_game_winner': tournament.final_game.winner.username if tournament.final_game and tournament.final_game.winner else None,
                'start_time': tournament.start_time,
                'end_time': tournament.end_time,
            }
            tournaments_data.append(tournament_data)

        return Response(tournaments_data, status=status.HTTP_200_OK)



class CreateFinal(APIView):


    def post(self, request):
        data = request.data
        player1_username = data.get('player1_username')
        player2_username = data.get('player2_username')
        tournament_id = data.get('tournament_id')

        # Verificar que los jugadores existen y están conectados
        player1 = get_object_or_404(MyUser, username=player1_username, is_connected=True)
        player2 = get_object_or_404(MyUser, username=player2_username, is_connected=True)

        # Verificar que el torneo existe
        tournament = get_object_or_404(Tournament, id=tournament_id)

        # Crear la partida final
        final_game = Game.objects.create(
            player1=player1,
            player2=player2,
        )

        tournament.final_game = final_game
        tournament.save()

        serialized_tournament = {
            'id': tournament.id,
            'initiator': tournament.initiator.username,
            'player1': tournament.player1.username,
            'player2': tournament.player2.username,
            'player3': tournament.player3.username,
            'player4': tournament.player4.username,
            'game1': tournament.game1.id if tournament.game1 else None,
            'game2': tournament.game2.id if tournament.game2 else None,
            'final_game': final_game.id,
            'start_time': tournament.start_time,
            'end_time': tournament.end_time,
        }
        return JsonResponse(serialized_tournament, status=201)
    

class MyTournaments(APIView):
    def get(self, request):
        user = request.user

        tournaments = Tournament.objects.filter(
            Q(player1=user) | Q(player2=user) | Q(player3=user) | Q(player4=user),
            end_time__isnull=True
        )

        serialized_tournaments = []
        for tournament in tournaments:
            game1_id = tournament.game1.id if tournament.game1 else None
            game2_id = tournament.game2.id if tournament.game2 else None
            final_game_id = tournament.final_game.id if tournament.final_game else None

            game1_winner = tournament.game1.winner.username if tournament.game1 and tournament.game1.winner else None
            game2_winner = tournament.game2.winner.username if tournament.game2 and tournament.game2.winner else None
            final_game_winner = tournament.final_game.winner.username if tournament.final_game and tournament.final_game.winner else None

            pending_game_id = None
            if game1_winner is None and (tournament.player1 == user or tournament.player2 == user):
                pending_game_id = game1_id
            elif game2_winner is None and (tournament.player3 == user or tournament.player4 == user):
                pending_game_id = game2_id
            elif final_game_winner is None and (tournament.player1 == user or tournament.player2 == user or tournament.player3 == user or tournament.player4 == user):
                pending_game_id = final_game_id

            serialized_tournament = {
                'id': tournament.id,
                'player1': tournament.player1.username,
                'player2': tournament.player2.username,
                'game1_winner': game1_winner,
                'player3': tournament.player3.username,
                'player4': tournament.player4.username,
                'game2_winner': game2_winner,
                'final_game_id': final_game_id,
                'final_game_winner': final_game_winner,
                'start_time': tournament.start_time,
                'end_time': tournament.end_time,
                'pending_game_id': pending_game_id,
            }

            serialized_tournaments.append(serialized_tournament)

        return Response(serialized_tournaments, status=status.HTTP_200_OK)
