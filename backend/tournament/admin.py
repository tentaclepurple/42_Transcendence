from django.contrib import admin
from .models import Tournament

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'initiator', 'game1_id', 'game2_id', 'final_game_id', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('initiator__username', 'player1__username', 'player2__username', 'player3__username', 'player4__username')

    # Para mostrar los IDs de las partidas en la lista
    def game1_id(self, obj):
        return obj.game1.id if obj.game1 else None
    game1_id.short_description = 'Game 1 ID'

    def game2_id(self, obj):
        return obj.game2.id if obj.game2 else None
    game2_id.short_description = 'Game 2 ID'

    def final_game_id(self, obj):
        return obj.final_game.id if obj.final_game else None
    final_game_id.short_description = 'Final Game ID'


admin.site.register(Tournament, TournamentAdmin)
