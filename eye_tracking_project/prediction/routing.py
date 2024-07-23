# prediction/routing.py
from django.urls import path
from . import consumers_image, consumers_video

websocket_urlpatterns = [
    path('ws/predict/image/', consumers_image.ImagePredictionConsumer.as_asgi()),
    path('ws/predict/video/', consumers_video.VideoConsumer.as_asgi()),  # 仍然通过 WebSocket 处理视频请求

]
