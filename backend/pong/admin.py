from django.contrib import admin
from .models import Game, Point

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'winner', 'created_at', 'started_at', 'finished_at', 'legit')
    list_filter = ('player1', 'player2', 'winner', 'legit')
    search_fields = ('player1__username', 'player2__username')
    date_hierarchy = 'created_at'

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'game_id', 'player', 'x', 'y', 'scored_at')
    list_filter = ('game', 'player')
    search_fields = ('game__id', 'player__username')
    date_hierarchy = 'scored_at'

    def game_id(self, obj):
        return obj.game.id

    game_id.short_description = 'Game ID'
