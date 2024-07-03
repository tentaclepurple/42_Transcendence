# FT_Trascendence

## Use:

-en raiz-
make
make exec

-dentro del contenedor-
cd app/backend
make pip
make mig
make suser
make run

-para desactivar el proceso de 2fa (enviar codigo al email etc)-
en backend/urls.py

comentar path de CustomRegisterView
#path('auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
path('auth/registration/', include('dj_rest_auth.registration.urls')),