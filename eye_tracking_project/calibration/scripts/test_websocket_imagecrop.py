import asyncio
import websockets
import base64
import json
import os

async def test_image_prediction(image_path, image_name):
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
                processed_image_path = os.path.join('processed_images', f'processed_{image_name}')
                os.makedirs('processed_images', exist_ok=True)
                with open(processed_image_path, 'wb') as f:
                    f.write(processed_image_data)
                print(f"Processed image saved as '{processed_image_path}'")

            if 'coordinates' in response_data and response_data['coordinates']:
                result["success"] = True
                result["coordinates"] = response_data['coordinates']

    return result

async def test_video_playback(video_id):
    uri = "ws://localhost:8000/ws/predict/video/"
    result = {"video_id": video_id, "success": False, "video_url": None}

    async with websockets.connect(uri) as websocket:
        message = json.dumps({"video_id": video_id})
        await websocket.send(message)

        response = await websocket.recv()
        response_data = json.loads(response)

        if 'video_url' in response_data:
            result["success"] = True
            result["video_url"] = response_data['video_url']
            print(f"Video URL received: {response_data['video_url']}")

    return result

async def main():
    # Test image prediction
    image_dir = "images"
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') and f.startswith('image')]

    image_tasks = []
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        image_tasks.append(test_image_prediction(image_path, image_file))

    image_results = await asyncio.gather(*image_tasks)

    print("Image Prediction Results:")
    for result in image_results:
        print(result)

    # Test video playback
    video_ids = ["video1", "video2"]  # You can add more video IDs here

    video_tasks = [test_video_playback(video_id) for video_id in video_ids]

    video_results = await asyncio.gather(*video_tasks)

    print("Video Playback Results:")
    for result in video_results:
        print(result)

if __name__ == "__main__":
    asyncio.run(main()) 