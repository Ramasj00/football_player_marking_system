import os
import random
import shutil

# Paths
base_dir = "yolo_files"
images_dir = os.path.join(base_dir, "images")
labels_dir = os.path.join(base_dir, "labels")

# Train, Val, Test folders
split_dirs = ["train", "val", "test"]
for d in split_dirs:
    os.makedirs(os.path.join(base_dir, d, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, d, "labels"), exist_ok=True)

# Get list of image filenames
images = [f for f in os.listdir(images_dir) if f.endswith(".jpg")]

# Shuffle and split
random.shuffle(images)
train_split = int(0.7 * len(images))
val_split = int(0.9 * len(images))

train_files = images[:train_split]
val_files = images[train_split:val_split]
test_files = images[val_split:]

# Move files
def move_files(file_list, subset):
    for file in file_list:
        shutil.move(os.path.join(images_dir, file), os.path.join(base_dir, subset, "images", file))
        label_file = file.replace(".jpg", ".txt")
        if os.path.exists(os.path.join(labels_dir, label_file)):
            shutil.move(os.path.join(labels_dir, label_file), os.path.join(base_dir, subset, "labels", label_file))

move_files(train_files, "train")
move_files(val_files, "val")
move_files(test_files, "test")

print("Dataset split completed!")
