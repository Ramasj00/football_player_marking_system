from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data="yolo_files/cr7_dataset.yaml", epochs=50, batch=8, imgsz=640)
