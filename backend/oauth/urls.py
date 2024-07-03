#oauth/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('authorize/', views.authorize, name='authorize'),  
    path('callback/', views.callback, name='callback'),
    path('campuses/', views.get_campuses, name='campuses'),
]

