from rest_framework import serializers
from .models import Statistic
from users.models import MyUser as User

class UserStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ('id', 'user', 'elo', 'games_played', 'games_won')

    def create(self, validated_data):
        user = User.objects.get(user=self.context['request'].user)
        statistic = Statistic.objects.create(**validated_data)
        statistic.user = user
        statistic.save()

        return statistic
