# del_labels.py
import os

images_dir = 'images'  # Путь к папке с изображениями
labels_dir = 'labels'  # Путь к папке с метками

# Получение списка всех файлов изображений, оставшихся после удаления
remaining_images = set(os.listdir(images_dir))

# Проверка файлов в папке labels
label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]

for file in label_files:
    # Создание имени соответствующего файла изображения
    corresponding_image = file.replace('.txt', '.png')
    if corresponding_image not in remaining_images:
        file_path = os.path.join(labels_dir, file)
        os.remove(file_path)  # Удаление файла
