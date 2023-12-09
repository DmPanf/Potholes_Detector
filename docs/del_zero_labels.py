# del_zero_labels.py
import os

labels_dir = 'labels'  # Путь к папке с метками
images_dir = 'images'  # Путь к папке с изображениями

# Получение списка всех файлов меток
label_files = os.listdir(labels_dir)

for file in label_files:
    label_path = os.path.join(labels_dir, file)
    
    # Проверка, является ли файл нулевой длины
    if os.path.getsize(label_path) == 0:
        os.remove(label_path)  # Удаление нулевого файла меток

        # Создание имени соответствующего файла изображения
        image_name = file.replace('.txt', '.png')
        image_path = os.path.join(images_dir, image_name)

        # Удаление соответствующего файла изображения, если он существует
        if os.path.exists(image_path):
            os.remove(image_path)
