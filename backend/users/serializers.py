from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from backend.settings import logger
from backend.settings import logger


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class CustomRegisterSerializer(RegisterSerializer):
    avatar = serializers.ImageField(write_only=True, required=False)
    nickname = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ['username', 'is_connected', 'is_42', 'avatar', 'nickname']
    
    def validate_nickname(self, value):
        logger.info(f"Validating nickname: {value}")
        if MyUser.objects.filter(nickname=value).exists():
            logger.error("Nickname already exists")
            raise serializers.ValidationError("Nickname already exists")
        return value

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['avatar'] = self.validated_data.get('avatar', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        return data

    def save(self, request):
        user = super().save(request)
        self.is_valid(raise_exception=True)
        cleaned_data = self.get_cleaned_data()
        user.nickname = self.validated_data.get('nickname', None)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.avatar = avatar
        user.is_42 = False
        user.save()
        return user

    def custom_signup(self, request, user):
        avatar = self.validated_data.get('avatar')
        if avatar:
            user.avatar = avatar
        user.is_42 = True
        return user



class UserSerializer(serializers.ModelSerializer):
    is_connected = serializers.BooleanField(read_only=True)
    avatar = serializers.SerializerMethodField()
    #is_42 = serializers.BooleanField(read_only=True)
    friends = serializers.StringRelatedField(many=True)
    blocked_users = serializers.StringRelatedField(many=True)
    chat_invitation = serializers.BooleanField(read_only=True)  

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'is_connected', 'is_42', 'avatar', 'friends', 'nickname', 'blocked_users', 'chat_invitation']

    def get_avatar(self, obj):
        request = self.context.get('request', None)
        if request and obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)
        
        return None
    
    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar', None)
        if avatar:
            instance.avatar = avatar
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
        

class AddRemoveFriendSerializer(serializers.Serializer):
    friend_username = serializers.CharField()



class BlockUnblockUserSerializer(serializers.Serializer):
    block_username = serializers.CharField(max_length=150)
