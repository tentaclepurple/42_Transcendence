from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import MyUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


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

    class Meta:
        model = MyUser
        fields = ['username', 'is_connected', 'is_42', 'avatar']
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['avatar'] = self.validated_data.get('avatar', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.save()
        return user
    
    def save(self, request):
        user = super().save(request)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.avatar = avatar
        user.is_42 = True
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
    #is_42 = serializers.BooleanField(read_only=True)
    friends = serializers.StringRelatedField(many=True)

    class Meta:
        model = MyUser
        fields = ['username', 'is_connected', 'is_42', 'avatar', 'friends']

class AddRemoveFriendSerializer(serializers.Serializer):
    friend_username = serializers.CharField()
