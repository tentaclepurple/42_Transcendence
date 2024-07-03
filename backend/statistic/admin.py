from django.contrib import admin
from .models import Statistic

# Register your models here.

class StatisticAdmin(admin.ModelAdmin):
	list_display = ('user', 'elo', 'games_played', 'games_won')
	search_fields = ('user__username',)

admin.site.register(Statistic, StatisticAdmin)
