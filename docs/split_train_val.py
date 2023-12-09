# split_train_val.py
import os
import shutil
import random

# Настройка путей к папкам
images_dir = 'images'
labels_dir = 'labels'
train_images_dir = 'train/images'
train_labels_dir = 'train/labels'
val_images_dir = 'val/images'
val_labels_dir = 'val/labels'

# Создание папок для наборов данных train и val
for dir in [train_images_dir, train_labels_dir, val_images_dir, val_labels_dir]:
    os.makedirs(dir, exist_ok=True)

# Получение списка всех файлов изображений
image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]
random.shuffle(image_files)  # Перемешивание списка файлов

# Определение точки разделения на train и val
split_point = int(0.9 * len(image_files))

# Разделение файлов на train и val
train_files = image_files[:split_point]
val_files = image_files[split_point:]

# Функция для перемещения файлов
def move_files(files, src_images_dir, src_labels_dir, dest_images_dir, dest_labels_dir):
    for file in files:
        image_path = os.path.join(src_images_dir, file)
        label_path = os.path.join(src_labels_dir, file.replace('.png', '.txt'))
        
        shutil.move(image_path, os.path.join(dest_images_dir, file))
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(dest_labels_dir, file.replace('.png', '.txt')))

# Перемещение файлов в соответствующие папки
move_files(train_files, images_dir, labels_dir, train_images_dir, train_labels_dir)
move_files(val_files, images_dir, labels_dir, val_images_dir, val_labels_dir)
