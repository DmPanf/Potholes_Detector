##

curl -X 'GET' \
  'http://0.0.0.0:8001/modes' \
  -H 'accept: application/json'


{
  "Modes_List": [
    "Basic",
    "Grid",
    "HQ-SAM",
    "YOLOv8"
  ],
  "Active_Mode": "Grid"
}


## 

curl -X 'POST' \
  'http://0.0.0.0:8001/skyline?skyline=28' \
  -H 'accept: application/json' \
  -d ''


{
  "Skyline": "28"
}


##

curl -X 'GET' \
  'http://0.0.0.0:8001/info' \
  -H 'accept: application/json'

{
  "Project 2023": "🔹 Potholes Detection [Moscow, 2023 г.]\n🔹 FastAPI Server with YOLOv8\n🔹 Client-Server Architecture with asynchronous requests"
}


##

curl -X 'POST' \
  'http://0.0.0.0:8001/modes/YOLOv8' \
  -H 'accept: application/json' \
  -d ''

{
  "Active_Mode": "YOLOv8"
}


##

curl -X 'GET' \
  'http://0.0.0.0:8001/models' \
  -H 'accept: application/json'

{
  "Models": [
    "YOLOv8Medium_80cls.pt",
    "ds1_yolov8l_1280_60e.pt",
    "ds1_yolov8m_1280_100e.pt",
    "ds1_yolov8n_1440_60e.pt",
    "ds1_yolov8s_1280_100e.pt",
    "ds1_yolov8s_1440_60e.pt"
  ]
}


##
curl -X 'POST' \
  'http://0.0.0.0:8001/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@img00.jpg;type=image/jpeg' \
  -F 'mdl_name=ds1_yolov8n_1440_60e.pt'


{
  "image": "...=",
  "results": {
    "model_name": "ds1_yolov8n_1440_60e.pt",
    "mode": "Grid",
    "object_count": 14,
    "max_box_width": 368,
    "confidence": 0.77,
    "inference": 307.7,
    "processing_time": 1.95,
    "current_time": "2023-11-21 02:23:13",
    "latitude": -2.872292,
    "longitude": -102.939632,
    "gpu_info": "GeForce RTX 3090 Ti",
    "system_ram": "128 GiB"
  }
}




