## Project Stages

### Calibration Stage

**Objective**: To send user's calibration images and data to the machine learning model for training purposes.

1. **User Setup**: The user positions their head in a frame and looks at different spots for calibration.
2. **Data Collection**: The frontend sends real-time images to the backend at 30 frames per second.
3. **Image Processing**: The backend processes these images, crops the eye area, and sends them to the machine learning model for training. The goal is to learn the user's eye movement patterns.

### Prediction Stage

**Objective**: To predict the eye gaze spot coordinates based on the trained model.

1. **Data Collection**: Similar to the calibration stage, the frontend sends real-time images to the backend at 30 frames per second.
2. **Image Processing**: The backend processes the images, crops the eye area, and sends them to the machine learning model for prediction. The model predicts the eye gaze spot coordinates and display heatmap on video.
3. **Video Playback**:  The backend sends the corresponding video URL to the frontend for playback.

## Setting Up the Environment

1. Clone the repository:

```sh
    git clone <repository_url>
    cd eye_tracking_project
```

2. Create and activate a virtual environment:

```sh
    python3 -m venv new_env
    source new_env/bin/activate
```

3. Install dependencies:

```sh
    pip install -r requirements.txt
```

## Running the Server

To start the server using Daphne:

```sh
      daphne -p 8000 -b 0.0.0.0 eye_tracking_project.asgi:application  

## Testing the Calibration Stage
```sh
    cd eye_tracking_project/calibration/scripts
    python test_websocket_imagecrop.py
```
## Testing the Prediction Stage
```sh
    cd eye_tracking_project/prediction/script
    python test_prediction.py
```
