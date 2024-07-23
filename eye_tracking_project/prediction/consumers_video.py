# prediction/consumers_video.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings 

# 假设视频文件存储在服务器的 'videos' 目录下
video_mapping = {
    "video1": "001_h264_1K.mp4",
    "video2": "002_h264_1K.mp4",
    # 添加更多视频ID与路径的对应关系
}

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            video_id = data.get('video_id')

            if not video_id:
                raise ValueError("Invalid video ID")

            video_url = self.get_video_url(video_id)

            if not video_url:
                raise ValueError("Video not found")

            response = {
                'video_url': video_url
            }

            await self.send(text_data=json.dumps(response))

        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
            await self.close()

    def get_video_url(self, video_id):
        # 根据 video_id 获取视频路径
        video_path = video_mapping.get(video_id)

        if not video_path:
            return None

        # 生成视频 URL，假设服务器域名为 example.com
        # video_url = f"http://127.0.0.1:8000/{video_path}"
        video_url = f"{settings.MEDIA_URL}{video_path}"
        return video_url