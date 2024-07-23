import asyncio
import websockets
import base64
import json
import os

# 图像测试函数
async def test_image_websocket(image_path, image_name):
    uri = "ws://localhost:8000/ws/predict/image/"
    result = {"image": image_name, "success": False, "coordinates": None}

    async with websockets.connect(uri) as websocket:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            message = json.dumps({
                "message": f"data:image/jpeg;base64,{image_data}"
            })
            await websocket.send(message)

            response = await websocket.recv()
            response_data = json.loads(response)

            if 'image' in response_data:
                processed_image_data = base64.b64decode(response_data['image'].split(',')[1])
                processed_image_path = os.path.join('../../images', f'processed_{image_name}')
                with open(processed_image_path, 'wb') as f:
                    f.write(processed_image_data)
                print(f"Processed image saved as '{processed_image_path}'")

            if 'coordinates' in response_data and response_data['coordinates']:
                result["success"] = True
                result["coordinates"] = response_data['coordinates']

    return result

# 视频测试函数
async def test_video_websocket(video_id):
    uri = "ws://localhost:8000/ws/predict/video/"
    result = {"video_id": video_id, "success": False, "video_url": None}

    async with websockets.connect(uri) as websocket:
        message = json.dumps({
            "video_id": video_id
        })
        await websocket.send(message)

        response = await websocket.recv()
        response_data = json.loads(response)

        if 'video_url' in response_data:
            video_url = response_data['video_url']
            result["success"] = True
            result["video_url"] = video_url
            print(f"Received video URL: {video_url}")

    return result

# 主函数
async def main():
    # 图像测试
    image_dir = "../../images"
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') and f.startswith('image')]
    image_tasks = []
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        image_tasks.append(test_image_websocket(image_path, image_file))
    
    image_results = await asyncio.gather(*image_tasks)

    # 打印图像测试结果
    for result in image_results:
        if result["success"]:
            print(f"Image: {result['image']}, Coordinates: {result['coordinates']}")
        else:
            print(f"Image: {result['image']} - Failed to detect eyes")

    # 视频测试
    video_ids = ["video1", "video2"]  # 请根据实际情况填写视频ID列表
    video_tasks = []
    for video_id in video_ids:
        video_tasks.append(test_video_websocket(video_id))
    
    video_results = await asyncio.gather(*video_tasks)

    # 打印视频测试结果
    for result in video_results:
        if result["success"]:
            print(f"Video ID: {result['video_id']}, Video URL: {result['video_url']}")
        else:
            print(f"Video ID: {result['video_id']} - Failed to get video URL")

if __name__ == "__main__":
    asyncio.run(main())