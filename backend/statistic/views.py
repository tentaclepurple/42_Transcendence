from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Statistic
from .serializers import UserStatisticSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class UserStatisticListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Statistic.objects.all()
    serializer_class = UserStatisticSerializer