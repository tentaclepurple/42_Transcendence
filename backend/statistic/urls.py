from django.urls import path
from .views import UserStatisticListCreateView

urlpatterns = [
    path('', UserStatisticListCreateView.as_view(), name='statistic_list_create'),
]