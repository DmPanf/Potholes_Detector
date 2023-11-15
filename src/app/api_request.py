import requests
import os

# to change the Directory
#os.chdir('/home/bunta/ARCHIVE/Projects.Python/3.Screening_System/y2.Simple.FastAPI-models/images')
os.chdir('./images')
print("\n\nCurrent Directory:", os.getcwd())

# URL of FastAPI Server
url = "http://0.0.0.0:8001/predict/"

# Model Name
mdl_name = "ds1_yolov8s_1280_100e.pt"

# Files to be processed
files = {'file': ('11.jpg', open('11.jpg', 'rb'), 'image/jpeg')}

# sending POST-requests
response = requests.post(url, files=files, data={'mdl_name': mdl_name})

# Status Code
print(response.status_code)

# Save Results
if response.status_code == 200:
    with open('result.jpg', 'wb') as f:
        f.write(response.content)
else:
    print("Error:", response.text)
