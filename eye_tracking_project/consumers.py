import json
import base64
from random import sample
import cv2
import numpy as np
import requests  # 用于向API端点发送请求
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
import os  # 用于文件操作

logger = logging.getLogger(__name__)

class DispatcherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("DispatcherConsumer: WebSocket 连接已建立")
        await self.accept()

    async def disconnect(self, close_code):
        logger.debug(f"DispatcherConsumer: WebSocket 连接关闭: {close_code}")

    async def receive(self, text_data):
        logger.debug(f"DispatcherConsumer 收到数据: {text_data}")
        try:
            if text_data.startswith('C'):
                await self.handle_calibration(text_data[1:])
            elif text_data.startswith('P'):
                await self.handle_image_prediction(text_data[1:])
            elif text_data.startswith('RequestVideoURL'):
                request_data = text_data.split(':')
                if len(request_data) == 2 and request_data[0] == "RequestVideoURL":
                    try:
                        num_videos = int(request_data[1])
                        await self.handle_video_request(num_videos)
                    except ValueError:
                        await self.send(text_data=json.dumps({'error': '请求的视频数量无效'}))
                else:
                    await self.send(text_data=json.dumps({'error': '无效数据'}))
            else:
                await self.send(text_data=json.dumps({'error': '无效数据'}))
        except Exception as e:
            logger.error(f"处理数据时出错: {e}")
            await self.send(text_data=json.dumps({'error': str(e)}))
            await self.close()

    async def handle_calibration(self, text_data):
        logger.debug("处理校准数据")
        data = json.loads(text_data)
        image_data = base64.b64decode(data['image'].split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("图像解码失败")

        image = cv2.resize(image, (320, 240))
        calibration_spot = data.get('calibration_spot', [0, 0])
        cropped_image, coordinates = self.detect_and_crop_eye_pair(image)

        # 生成文件名，包括校准点坐标
        file_name = f'processed_image_{calibration_spot[0]}_{calibration_spot[1]}.jpg'
        file_path = os.path.join('your_save_directory', file_name)

        # 保存裁剪后的图片
        cv2.imwrite(file_path, cropped_image)
        logger.debug(f"图像已保存为: {file_path}")

        # 将处理后的图像发送到机器学习模型
        _, buffer = cv2.imencode('.jpg', cropped_image)
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
        self.send_data_to_model(processed_image_base64, calibration_spot, 'calibration')

    async def handle_image_prediction(self, text_data):
        logger.debug("处理图片预测数据")
        data = json.loads(text_data)
        image_data = base64.b64decode(data['image'].split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("图像解码失败")

        image = cv2.resize(image, (320, 240))
        cropped_image, coordinates = self.detect_and_crop_eye_pair(image)

        cropped_image = cv2.resize(cropped_image, (224, 224))
        _, buffer = cv2.imencode('.jpg', cropped_image)
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

        # 发送处理后的图像到机器学习模型，进行预测
        self.send_data_to_model(processed_image_base64, None, 'prediction')

    def detect_and_crop_eye_pair(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
        # 应用直方图均衡化
        gray = cv2.equalizeHist(gray)
        
        eye_pair_cascade_path = 'cascades/haarcascade_mcs_eyepair_big.xml'
        eye_pair_cascade = cv2.CascadeClassifier(eye_pair_cascade_path)

        eyes = eye_pair_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,  # 尝试调整这个值，比如 1.05 或 1.2
            minNeighbors=6,   # 尝试增加这个值以减少错误检测
            minSize=(20, 20)  # 视情况调整最小尺寸
        )
        coordinates = []
        cropped_image = image

        for (x, y, w, h) in eyes:
            coordinates.append((x, y, x + w, y, x, y + h, x + w, y + h))
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # 裁剪出眼睛区域
            cropped_image = image[y:y + h, x:x + w]

        return cropped_image, coordinates
                

    def send_data_to_model(self, image_base64, calibration_spot, stage):
        try:
            payload = {
                'image': image_base64,
                'stage': stage,
            }
            if stage == 'calibration':
                payload['calibration_spot'] = calibration_spot

            response = requests.post(
                'http://localhost:8000/api/model/', 
                json=payload
            )

            if response.status_code == 200:
                logger.debug("成功将数据发送到模型端点")
            else:
                logger.error(f"发送数据到模型失败: {response.status_code}")

        except Exception as e:
            logger.error(f"发送数据到模型时出错: {e}")

    async def handle_video_request(self, num_videos):
        all_video_urls = [
            "../videos/001_h264_1K.mp4",
            "../videos/002_h264_1K.mp4",
            # 添加更多视频URL
        ]

        if num_videos > len(all_video_urls):
            num_videos = len(all_video_urls)

        selected_videos = sample(all_video_urls, num_videos)

        response = {
            'video_urls': selected_videos
        }
        await self.send(text_data=json.dumps(response))