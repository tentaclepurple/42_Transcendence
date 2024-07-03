from .serializers import CustomRegisterSerializer, UserSerializer, AddRemoveFriendSerializer
from .models import MyUser
from twofa.models import TwoFaCode
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dj_rest_auth.registration.views import RegisterView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
import json


@api_view(['GET'])
def user_list(request, ):
    users = MyUser.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_friend(request):
    serializer = AddRemoveFriendSerializer(data=request.data)
    if serializer.is_valid():
        friend_username = serializer.validated_data['friend_username']
        user = request.user 
        friend = get_object_or_404(MyUser, username=friend_username)
        user.friends.add(friend)
        return Response({'success': True, 'message': f"{friend_username} added as friend."})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def remove_friend(request):
    serializer = AddRemoveFriendSerializer(data=request.data)
    if serializer.is_valid():
        friend_username = serializer.validated_data['friend_username']
        user = request.user 
        friend = get_object_or_404(MyUser, username=friend_username)
        user.friends.remove(friend)
        return Response({'success': True, 'message': f"{friend_username} removed as friend."})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def friend_list(request):
    user = request.user
    friends = user.friends.all()
    serializer = UserSerializer(instance=friends, many=True)
    return Response(serializer.data)


class UpdateUserView(APIView):

    def post(self, request):
        user = request.user
        data = request.data

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'avatar' in data:
            user.avatar = data['avatar']

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({"detail": "User registered successfully. Please log in."},
            status=201,
            headers=headers)
    
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return serializer.custom_signup(self.request, user)


class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        code = data.get('code')

        twofa_code = None

        try:
            user = MyUser.objects.get(username=username)
            if not user.is_42:
                twofa_code = TwoFaCode.objects.get(user=user, code=code)
            
        except Exception as e:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            token_auth, created = Token.objects.get_or_create(user=user)

            user.is_connected = True
            user.save()
            
            if twofa_code is not None:
                twofa_code.delete()

            return JsonResponse({'access_token': access_token, 'refresh_token': refresh_token, 'token_auth': token_auth.key})

        return JsonResponse({'error': 'Invalid credentials'}, status=400)
