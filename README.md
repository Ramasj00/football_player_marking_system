# Football Game Player Marking

This project is designed to mark players in football game videos using YOLO for object detection and a React frontend for visualization.

# HOW TO USE
1. run backend/flask_api.py and npm run dev frontend.

2. Input video

3. Click Mark Player button

4. View processed result

# Project Structure

## Backend

The backend is responsible for processing video files, extracting frames, and training the YOLO model.

### YOLO Model Training

The YOLO model is trained using the `yolo_model_training.py` script.

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data="yolo_files/cr7_dataset.yaml", epochs=50, batch=8, imgsz=640)
```

## Frontend

The frontend is a React application created with Vite, located in the football_game_player_marking directory.

![image](https://github.com/user-attachments/assets/a6b60f01-f6ec-4f15-ac1e-fcf1a9ed7fb2)

![image](https://github.com/user-attachments/assets/7b41fbc6-4d5d-420b-8b5d-6eb62a132b25)

![image](https://github.com/user-attachments/assets/62611ad3-fea1-488c-92c6-5b1938409306)
