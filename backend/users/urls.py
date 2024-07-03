from django.urls import path
from . import views
from .views import UpdateUserView, ConnectUserView, DisconnectUserView

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('profile/', views.user_profile, name='user_profile'),
	path('add_friend/', views.add_friend, name='add_friend'),
    path('remove_friend/', views.remove_friend, name='remove_friend'),
    path('friend_list/', views.friend_list, name='friend_list'),
    path('block_user/', views.block_user, name='block_user'),
    path('unblock_user/', views.unblock_user, name='unblock_user'),
    path('update/', UpdateUserView.as_view(), name='update_user'),
    path('profile/delete/', UpdateUserView.as_view(), name='delete_profile'),  # Use UpdateUserView here
    path('connect/', ConnectUserView.as_view(), name='connect'),
    path('disconnect/', DisconnectUserView.as_view(), name='disconnect'),
]