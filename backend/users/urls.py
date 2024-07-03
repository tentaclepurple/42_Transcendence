from django.urls import path
from . import views
from .views import UpdateUserView

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
	path('add_friend/', views.add_friend, name='add_friend'),
    path('remove_friend/', views.remove_friend, name='remove_friend'),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('update/', UpdateUserView.as_view(), name='update_user'),
]
