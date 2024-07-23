# prediction/consumers_image.py
import json
import base64
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer

class ImagePredictionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            image_data = base64.b64decode(data['message'].split(',')[1])
            np_arr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Image decoding failed")

            # 统一调整图像尺寸
            image = cv2.resize(image, (640, 480))

            # 图像处理和预测
            cropped_image, coordinates = self.detect_and_crop_eye_pair(image)

            # 将裁剪后的图像调整尺寸
            cropped_image = cv2.resize(cropped_image, (224, 224))

            # 将处理后的图像编码为Base64
            _, buffer = cv2.imencode('.jpg', cropped_image)
            processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

            # 将坐标转为JSON可序列化格式
            coordinates = [[int(coord) for coord in rect] for rect in coordinates]

            # 构建返回给前端的响应
            response = {
                'image': f'data:image/jpeg;base64,{processed_image_base64}',
                'coordinates': coordinates
            }

            await self.send(text_data=json.dumps(response))

        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
            await self.close()

    def detect_and_crop_eye_pair(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eye_pair_cascade_path = 'cascades/haarcascade_mcs_eyepair_big.xml'
        eye_pair_cascade = cv2.CascadeClassifier(eye_pair_cascade_path)

        eyes = eye_pair_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        coordinates = []
        cropped_image = image

        for (x, y, w, h) in eyes:
            coordinates.append((x, y, x + w, y, x, y + h, x + w, y + h))
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, f"({x},{y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(image, f"({x + w},{y})", (x + w, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(image, f"({x},{y + h})", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(image, f"({x + w},{y + h})", (x + w, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            cropped_image = image[y:y + h, x:x + w]

        return cropped_image, coordinates