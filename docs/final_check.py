# final_check.py

import os
train_images_dir = 'train/images' # Пути к папкам
train_labels_dir = 'train/labels'
val_images_dir = 'val/images'
val_labels_dir = 'val/labels'

def count_files_and_check_labels(images_dir, labels_dir):
    # Получение списков файлов
    image_files = set(os.listdir(images_dir))
    label_files = set(os.listdir(labels_dir))

    # Подсчет изображений
    num_images = len(image_files)

    # Проверка, что каждый файл меток имеет соответствующий файл изображения
    missing_images = [label_file.replace('.txt', '.png') for label_file in label_files if label_file.replace('.txt', '.png') not in image_files]

    return num_images, missing_images

# Получение данных и проверка для train
train_images_count, train_missing_images = count_files_and_check_labels(train_images_dir, train_labels_dir)

# Получение данных и проверка для val
val_images_count, val_missing_images = count_files_and_check_labels(val_images_dir, val_labels_dir)

# Вывод результатов
print(f"Number of images in 'train': {train_images_count}")
print(f"Number of images in 'val': {val_images_count}")
print(f"Total number of images: {train_images_count + val_images_count}")


# Проверка на недостающие изображения
if train_missing_images or val_missing_images:
    print("Missing image files for some labels detected!")
    if train_missing_images:
        print(f"Missing in 'train': {train_missing_images}")
    if val_missing_images:
        print(f"Missing in 'val': {val_missing_images}")
else:
    print("All label files have corresponding image files.")
