from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/test/', consumers.CalibrationConsumer.as_asgi()),
]