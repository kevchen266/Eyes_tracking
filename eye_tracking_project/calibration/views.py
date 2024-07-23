# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# import cv2
# import os
# import numpy as np
# import csv
# from django.conf import settings
# from django.core.files.storage import default_storage

# class EyeTrackingDataView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         try:
#             video_file = request.FILES['video']
#             participant_id = request.data.get('participant_id')
#             participant_age = request.data.get('age')
#             participant_gender = request.data.get('gender')

#             # 保存上传的视频文件到 videos 文件夹
#             video_folder = settings.MEDIA_ROOT
#             if not os.path.exists(video_folder):
#                 os.makedirs(video_folder)

#             video_path = os.path.join(video_folder, video_file.name)
#             with default_storage.open(video_path, 'wb+') as destination:
#                 for chunk in video_file.chunks():
#                     destination.write(chunk)

#             # 进行校准步骤
#             calibration_data = self.calibrate(video_path)
#             if calibration_data is None:
#                 return Response({'error': '校准失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # 处理视频并生成 CSV 文件
#             csv_file_path = self.process_video(video_path, participant_id, participant_age, participant_gender, calibration_data)
#             print(f"生成的CSV文件路径: {csv_file_path}")  # 打印调试信息
#             if csv_file_path:
#                 csv_file_url = os.path.join(settings.MEDIA_URL, os.path.basename(csv_file_path))
#                 return Response({'csv_file_url': csv_file_url}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'error': 'CSV文件生成失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def calibrate(self, video_path):
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             print(f"无法打开视频文件进行校准: {video_path}")
#             return None

#         calibration_data = []
#         frame_rate = cap.get(cv2.CAP_PROP_FPS)
#         num_frames = int(frame_rate * 5)  # 获取5秒的视频帧数

#         for _ in range(num_frames):
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             eyes = self.detect_eyes(gray)
#             if eyes is not None and len(eyes) > 0:
#                 for (ex, ey, ew, eh) in eyes:
#                     eye_frame = gray[ey:ey+eh, ex:ex+ew]
#                     pupil_x, pupil_y = self.detect_pupil(eye_frame)
#                     calibration_data.append((pupil_x + ex, pupil_y + ey))

#         cap.release()

#         if len(calibration_data) > 0:
#             avg_pupil_x = sum([data[0] for data in calibration_data]) / len(calibration_data)
#             avg_pupil_y = sum([data[1] for data in calibration_data]) / len(calibration_data)
#             return (avg_pupil_x, avg_pupil_y)
#         else:
#             return None

#     def process_video(self, video_path, participant_id, participant_age, participant_gender, calibration_data):
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             print(f"无法打开视频文件: {video_path}")
#             return None

#         csv_data = []

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             eyes = self.detect_eyes(gray)
#             for eye in eyes:
#                 (x, y, w, h) = eye
#                 eye_frame = gray[y:y+h, x:x+w]
#                 pupil_x, pupil_y = self.detect_pupil(eye_frame, calibration_data)
                
#                 csv_data.append([participant_id, participant_age, participant_gender, x + pupil_x, y + pupil_y, w, h])

#         cap.release()

#         csv_file_path = os.path.splitext(video_path)[0] + '.csv'
#         with open(csv_file_path, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['participant_id', 'age', 'gender', 'pupil_x', 'pupil_y', 'eye_x', 'eye_y', 'eye_width', 'eye_height'])
#             writer.writerows(csv_data)

#         return csv_file_path

#     def detect_eyes(self, gray_frame):
#         eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#         eyes = eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#         return eyes

#     def detect_pupil(self, eye_frame, calibration_data=None):
#         # 使用高斯模糊减少噪声
#         blurred_frame = cv2.GaussianBlur(eye_frame, (7, 7), 0)
#         # 应用霍夫圆变换
#         circles = cv2.HoughCircles(
#             blurred_frame,
#             cv2.HOUGH_GRADIENT,
#             dp=1,
#             minDist=eye_frame.shape[0] / 8,
#             param1=50,
#             param2=30,
#             minRadius=5,
#             maxRadius=30
#         )

#         if circles is not None:
#             circles = np.uint16(np.around(circles))
#             for i in circles[0, :]:
#                 pupil_x = i[0]
#                 pupil_y = i[1]
#                 print(f"Detected pupil at: ({pupil_x}, {pupil_y})")  # 调试信息
#                 return pupil_x, pupil_y  # 返回圆心坐标 (pupil_x, pupil_y)
#         else:
#             # 使用校准数据调整检测结果
#             if calibration_data:
#                 print(f"Using calibration data for pupil position: {calibration_data}")  # 调试信息
#                 return calibration_data
#             else:
#                 center_x = eye_frame.shape[1] / 2
#                 center_y = eye_frame.shape[0] / 2
#                 print(f"Defaulting to center position: ({center_x}, {center_y})")  # 调试信息
#                 return center_x, center_y  # 如果没有检测到圆，返回眼睛区域的中心
