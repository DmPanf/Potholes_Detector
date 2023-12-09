# del_odd.py
import os

images_dir = 'images'  # Путь к папке с изображениями

# Получение списка всех файлов изображений
image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]

# Удаление всех нечетных изображений
for file in image_files:
    # Проверка, является ли номер изображения нечетным
    number_part = file.split('_')[-1].split('.')[0]  # Извлечение номера из названия файла
    if int(number_part) % 2 != 0:  # Проверка на нечетность
        file_path = os.path.join(images_dir, file)
        os.remove(file_path)  # Удаление файла
