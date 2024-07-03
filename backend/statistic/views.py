from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Statistic
from .serializers import UserStatisticSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from backend.settings import logger
from rest_framework.views import APIView
from users.models import MyUser as User


# Create your views here.

class UserStatisticListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Statistic.objects.all()
    serializer_class = UserStatisticSerializer

class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = request.user
        stats = user.statistics
        serializer = UserStatisticSerializer(stats)
        return Response(serializer.data)

class AllUserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = Statistic.objects.all().order_by('-elo')
        serializer = UserStatisticSerializer(stats, many=True)
        return Response(serializer.data)

class UserRankNumberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)
        if user_id:
            user = User.objects.get(id=user_id)
        else:
            user = request.user
        stats = Statistic.objects.all().order_by('-elo')
        rank = 1
        for stat in stats:
            if stat.user == user:
                break
            rank += 1
        return Response(rank)
