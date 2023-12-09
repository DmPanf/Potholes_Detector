# draw_random.py
import cv2
import matplotlib.pyplot as plt
import os
import random
#import matplotlib
#matplotlib.use('Qt5Agg')  # Или другой бэкенд, например 'Agg', 'Qt5Agg' и т.д.


def draw_boxes(img_path, label_path):
    # Чтение изображения
    img = cv2.imread(img_path)
    h, w, _ = img.shape

    # Чтение файла с метками
    with open(label_path, 'r') as file:
        for line in file:
            # Разбор строки метки
            class_id, center_x, center_y, width, height = map(float, line.split())

            # Преобразование нормализованных координат в пиксельные координаты
            x1 = int((center_x - width / 2) * w)
            y1 = int((center_y - height / 2) * h)
            x2 = int((center_x + width / 2) * w)
            y2 = int((center_y + height / 2) * h)

            # Рисование прямоугольника
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

    # Отображение изображения
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    cv2.imwrite('output.png', img)
    # plt.show()

# Выбор случайного изображения
images_dir = 'images'
labels_dir = 'labels'
random_image_name = random.choice(os.listdir(images_dir))
img_path = os.path.join(images_dir, random_image_name)
label_path = os.path.join(labels_dir, random_image_name.replace('.png', '.txt'))

# Визуализация
draw_boxes(img_path, label_path)
