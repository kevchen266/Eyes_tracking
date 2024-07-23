"""
ASGI config for eye_calibration_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eye_calibration_project.settings')

# application = get_asgi_application()
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from calibration.routing import websocket_urlpatterns as calibration_websocket_urlpatterns
from prediction.routing import websocket_urlpatterns as prediction_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eye_tracking_project.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            calibration_websocket_urlpatterns + prediction_websocket_urlpatterns
        )
    ),
})