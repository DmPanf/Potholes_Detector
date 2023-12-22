import requests
import os

# Переходим в нужную директорию
#os.chdir('/home/bunta/ARCHIVE/Projects.Python/3.Screening_System/y2.Simple.FastAPI-models/images')
os.chdir('./images')
print("\n\nCurrent Directory:", os.getcwd())

# URL FastAPI сервера
url = "http://0.0.0.0:8001/predict/"

# Имя модели
mdl_name = "ds1_yolov8s_1280_100e.pt"

# Подготовка файла
files = {'file': ('11.jpg', open('11.jpg', 'rb'), 'image/jpeg')}

# Отправляем POST-запрос
response = requests.post(url, files=files, data={'mdl_name': mdl_name})

# Выводим статус ответа
print(response.status_code)

# Сохраняем полученный файл, если ответ успешный
if response.status_code == 200:
    with open('result.jpg', 'wb') as f:
        f.write(response.content)
else:
    print("Error:", response.text)
