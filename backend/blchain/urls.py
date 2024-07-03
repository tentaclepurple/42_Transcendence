from django.urls import path
from .views import blchain_get_data, blchain_add_data
urlpatterns = [
    path('add/', blchain_add_data, name='blchain_add_data'),
    path('get/', blchain_get_data, name='blchain_get_data')
]
  