import asyncio
import websockets
import json
import base64
import os
import random

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws/test_dispatcher/"

    current_directory = os.path.dirname(os.path.abspath(__file__))
    images_folder = os.path.join(current_directory, "../../images")

    print(f"Images folder: {images_folder}")

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Generate 9 random calibration spots
        random_calibration_spots = [(random.randint(100, 500), random.randint(100, 500)) for _ in range(9)]

        # Test calibration stage
        for filename in os.listdir(images_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(images_folder, filename)

                # Read and encode the image file as base64
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

                for idx, calibration_spot in enumerate(random_calibration_spots):
                    calibration_data = {
                        "participant_id": "testUser1",
                        "image": f"data:image/jpeg;base64,{image_data}",
                        "age": 25,
                        "gender": 1,
                        "calibration_spot": calibration_spot
                    }

                    message = "C" + json.dumps(calibration_data)

                    print(f"Sending calibration image: {filename} at spot: {calibration_spot}")
                    await websocket.send(message)

                    print("Waiting for server response")
                    response = await websocket.recv()
                    print(f"Received response: {response}")

        # Test prediction stage
        for filename in os.listdir(images_folder):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(images_folder, filename)

                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

                prediction_data = {
                    "participant_id": "testUser1",
                    "image": f"data:image/jpeg;base64,{image_data}",
                    "age": 25,
                    "gender": 1,
                }

                message = "P" + json.dumps(prediction_data)

                print(f"Sending prediction image: {filename}")
                await websocket.send(message)

                print("Waiting for server response")
                response = await websocket.recv()
                print(f"Received response: {response}")

# Run the test script
asyncio.get_event_loop().run_until_complete(test_websocket())