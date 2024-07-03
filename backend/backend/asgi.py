import os
import django
from django.core.asgi import get_asgi_application

# Ensure the environment variable is set first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
if not django.apps.registry.apps.ready:
    django.setup()

import django
from django.core.asgi import get_asgi_application
# Ensure the environment variable is set first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
django.setup()
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat import routing as chat_routing
from pong import routing as pong_routing
from .tokenauth_middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                chat_routing.websocket_urlpatterns +
                pong_routing.websocket_urlpatterns
            )
        )
    )
})
