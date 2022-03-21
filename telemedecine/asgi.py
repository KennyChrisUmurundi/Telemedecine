import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import telemedecine.apps.telehealth.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videocall.settings")

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                telemedecine.apps.telehealth.routing.websocket_urlpatterns
            )
        ),
    }
)
