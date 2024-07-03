from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_convo, name='start_convo'),
    path('<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('', views.conversations, name='conversations'),
	path('accept_invitation/', views.accept_invitation, name='accept_invitation'),
    path('decline_invitation/', views.decline_invitation, name='decline_invitation'),
    path('check_invitation/', views.check_invitation, name='check_invitation'),
]
