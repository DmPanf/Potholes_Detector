# video2frames.py
import cv2
import os

# Путь к видеофайлу
video_path = 'v01p2.mp4'

# Создание объекта VideoCapture для чтения видео
cap = cv2.VideoCapture(video_path)

# Создание директории для сохранения кадров, если она еще не существует
frames_dir = 'frames'
os.makedirs(frames_dir, exist_ok=True)

# Индекс кадра
frame_idx = 0

while True:
    # Чтение кадра из видео
    ret, frame = cap.read()

    # Если кадр успешно прочитан
    if ret:
        # Формирование имени файла
        frame_name = f'v01p2_{frame_idx:06d}.png'
        frame_path = os.path.join(frames_dir, frame_name)

        # Сохранение кадра
        cv2.imwrite(frame_path, frame)

        # Увеличение индекса кадра
        frame_idx += 1
    else:
        break

# Освобождение ресурсов
cap.release()
