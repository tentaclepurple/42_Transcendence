from django.contrib import admin
from django.urls import path, include
from .views import home
from users.views import CustomLoginView, CustomRegisterView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('twofa/', include('twofa.urls')),
    path('admin/', admin.site.urls),
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('conversations/', include('chat.urls')),
    path('users/', include('users.urls')),
    path('pong/', include('pong.urls')),
    path('statistic/', include('statistic.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('oauth/', include('oauth.urls')),
    path('', home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
