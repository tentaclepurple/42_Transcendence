from django.urls import path
from .views import (
	UserStatisticListCreateView,
	UserStatsView, AllUserStatsView,
	UserRankNumberView,
)

urlpatterns = [
    path('', UserStatisticListCreateView.as_view(), name='statistic_list_create'),
	path('user-stats/', UserStatsView.as_view(), name='statistic_user_stats'),
	path('all-user-stats/', AllUserStatsView.as_view(), name='statistic_all_user_stats'),
	path('user-rank/', UserRankNumberView.as_view(), name='statistic_user_rank'),
]