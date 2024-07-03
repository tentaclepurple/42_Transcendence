from rest_framework import serializers
from .models import Statistic
from users.models import MyUser as User
from backend.settings import logger

class UserStatisticSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Statistic
        fields = ('id', 'user_id', 'user', 'username', 'elo', 'games_played', 'games_won')
        fields = '__all__'
        
    def create(self, validated_data):
        user = User.objects.get(user=self.context['request'].user)
        statistic = Statistic.objects.create(**validated_data)
        statistic.user = user
        statistic.save()

        return statistic
    
