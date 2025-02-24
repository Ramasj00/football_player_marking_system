import cv2
import os

video_path = "portugal_vs_spain.mp4"
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count == 10000:
        break
    # Save every nth frame (for example, every 10th frame) to reduce redundancy
    if frame_count % 10 == 0:
        cv2.imwrite(os.path.join(output_folder, f"frame_{frame_count}.jpg"), frame)
    frame_count += 1

cap.release()