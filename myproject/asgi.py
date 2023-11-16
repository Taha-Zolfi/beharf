import os
from django.conf import settings
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from myapp.consumers import VideoConsumer, websocket_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# اضافه کردن settings.configure()
# settings.configure()


application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'https': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)
