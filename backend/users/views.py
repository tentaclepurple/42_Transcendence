from .serializers import CustomRegisterSerializer, UserSerializer, AddRemoveFriendSerializer, BlockUnblockUserSerializer
from .models import MyUser
from django.contrib.auth import authenticate
from twofa.models import TwoFaCode
from rest_framework.response import Response
from rest_framework.decorators import api_view
from dj_rest_auth.registration.views import RegisterView
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

import json
from backend.settings import logger
from oauth.views import check_nickname, check_username, generate_random_nickname, generate_random_username

ACCEPTED_TYPES = "image"


# TODO merge with statistics
@api_view(['GET'])
def user_list(request, ):
    users = MyUser.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def user_profile(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['POST'])
def block_user(request):
    serializer = BlockUnblockUserSerializer(data=request.data)
    if serializer.is_valid():
        blocked_username = serializer.validated_data['block_username']
        user = request.user
        if user.username == blocked_username:
            return Response({'error': 'You cannot block yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        blocked_user = get_object_or_404(MyUser, username=blocked_username)
        user.blocked_users.add(blocked_user)
        return Response({'success': True, 'message': f"{blocked_username} has been blocked."}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unblock_user(request):
    serializer = BlockUnblockUserSerializer(data=request.data)
    if serializer.is_valid():
        blocked_username = serializer.validated_data['block_username']
        user = request.user
        if user.username == blocked_username:
            return Response({'error': 'You cannot unblock yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        blocked_user = get_object_or_404(MyUser, username=blocked_username)
        user.blocked_users.remove(blocked_user)
        return Response({'success': True, 'message': f"{blocked_username} has been unblocked."}, status=status.HTTP_200_OK)
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

        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if user.nickname != data.get('nickname', user.nickname):
            if MyUser.objects.filter(nickname=data.get('nickname', user.nickname)).exists():
                raise ValidationError({"nickname": ["Nickname already exists"]})
        user.nickname = data.get('nickname', user.nickname)
        avatar = data.get('avatar', None)

        if avatar and not isinstance(avatar, str) and ACCEPTED_TYPES in avatar.content_type:
            user.avatar = data['avatar']

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        if user is None:
            return Response({"Error":"Wrong password"}, 404)

        user.delete()
        return Response({"Message":"User deleted succesfully"}, 200)

    def validate_nickname(self, value):
        logger.info(f"Validating nickname: {value}")
        if MyUser.objects.filter(nickname=value).exists():
            logger.error("Nickname already exists")
            raise serializers.ValidationError("Nickname already exists")
        return value


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    
    def create(self, request, *args, **kwargs):
        logger.warning('Creating user')
        logger.warning(request.data)
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

    def post(self, request, *args, **kwargs):
        serializer = CustomRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            data = request.data.copy()
            if check_nickname(data.get("nickname")):
                data["nickname"] = generate_random_nickname()
            if check_nickname(data.get("username")):
                data["username"] = generate_random_username()
            serializer = CustomRegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save(request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ConnectUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_connected = True
        user.save()
        return Response({'message': 'User is now connected.'}, status=status.HTTP_200_OK)


class DisconnectUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_connected = False
        user.save()
        return Response({'message': 'User is now disconnected.'}, status=status.HTTP_200_OK)