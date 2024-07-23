import cv2
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt

def check_video_file(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return False

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))

    codec_str = ''.join([chr((codec >> 8 * i) & 0xFF) for i in range(4)])

    print(f"视频文件信息: {video_path}")
    print(f"帧数: {frame_count}")
    print(f"帧率: {frame_rate}")
    print(f"分辨率: {width}x{height}")
    print(f"编码器: {codec_str}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Check', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True

def upload_video_and_test_api(video_path, api_url, participant_info):
    print(f"Checking if video file exists at path: {video_path}")
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return

    print(f"Uploading video from path: {video_path}")
    files = {
        'video': open(video_path, 'rb'),
        'participant_id': (None, participant_info['participant_id']),
        'age': (None, participant_info['age']),
        'gender': (None, participant_info['gender']),
    }
    response = requests.post(api_url, files=files)

    # 打印响应的状态码和文本内容以进行调试
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # 尝试解析 JSON 响应
    try:
        response_json = response.json()
        print(response_json)
        return response_json
    except requests.exceptions.JSONDecodeError:
        print("Error: Received response is not a valid JSON")
        return None

def visualize_csv_data(csv_path):
    df = pd.read_csv(csv_path)
    print(df.head())

    # Create a trajectory plot for pupil and eye positions
    plt.figure(figsize=(10, 6))

    # Plot pupil trajectory
    plt.plot(df['pupil_x'], df['pupil_y'], marker='o', linestyle='-', color='blue', label='Pupil Trajectory')

    # Plot eye positions
    for index, row in df.iterrows():
        eye_x = row['eye_x']
        eye_y = row['eye_y']
        eye_width = row['eye_width']
        eye_height = row['eye_height']
        plt.plot(eye_x, eye_y, marker='x', color='red', label='Eye Position' if index == 0 else "")
        

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Pupil and Eye Trajectory')
    plt.legend()
    plt.gca().invert_yaxis()  # Invert y axis to match typical screen coordinates
    plt.show()

if __name__ == "__main__":
    video_path = '/Users/kev19/Desktop/Project/summer project/eyestracking/backend/eye_tracking_project/tracking/videos/testing.mov'
    api_url = 'http://127.0.0.1:8000/tracking/eye_tracking_data/'
    participant_info = {
        'participant_id': '123',
        'age': '25',
        'gender': 'male'
    }

    # Step 1: Check video file
    if check_video_file(video_path):
        # Step 2: Upload video and test API
        response = upload_video_and_test_api(video_path, api_url, participant_info)

        # Step 3: Visualize CSV data
        if response and 'csv_file_url' in response:
            csv_url = response['csv_file_url']
            csv_path = os.path.join('/Users/kev19/Desktop/Project/summer project/eyestracking/backend/eye_tracking_project/videos', os.path.basename(csv_url))
            visualize_csv_data(csv_path)
        else:
            print("Error: CSV file URL not found in the response.")
    else:
        print(f"视频文件 {video_path} 未找到，检测失败")
