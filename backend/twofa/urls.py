from django.urls import path
from .views import send_twofa_email, twofaform

urlpatterns = [
    path('', twofaform, name='twofa_form'),
    path('send-code/', send_twofa_email, name='send_twofa_email')
]
  