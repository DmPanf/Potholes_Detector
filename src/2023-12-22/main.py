from ultralytics import YOLO  # pip install ultralytics (https://github.com/ultralytics/ultralytics)
import cv2  # pip install opencv-python (https://pypi.org/project/opencv-python/)
import numpy as np  # pip install numpy (https://pypi.org/project/numpy/)
from PIL import Image  # pip install Pillow (https://pypi.org/project/Pillow/)
import io  # pip install io (https://pypi.org/project/io/)
# pip install fastapi (https://pypi.org/project/fastapi/)
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import base64  # pip install base64 (https://pypi.org/project/base64/)
import json  # pip install json (https://pypi.org/project/json/)
import glob  # (https://pypi.org/project/glob/)
import os  # (https://pypi.org/project/os/)
import time  # (https://pypi.org/project/time/)
import random  # (https://pypi.org/project/random/)
#import torch #torch.cuda.is_available = lambda : False  # принудительно использовать только CPU для PyTorch
from dotenv import load_dotenv, set_key
from pathlib import Path
from bboxes import draw_boxes  # external module for Basic Bounding Box
from grid import draw_trapezoid_grid  # external module for Grid
from yolov8 import yolo_box  # external module for YOLOv8
import tempfile
import sqlite3
import os
import csv
import rdflib

# Load environment variables
load_dotenv()
ENV_FILE = '.env'

# Authorization token for example. In a real application, this should be protected!
FAKE_TOKEN = os.getenv("FastAPI_TOKEN")  # "goodroad"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

default_mdl_path = './models/'  # Default path to models directory
default_sqlite3_path = './data/image_data.db'
KB_path = "./data/KB_V3_2.n3"

app = FastAPI(title="Potholes Detection System API", version="0.1.0", debug=True)  # Initialize FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to insert data into the database
def insert_image_data(image_data):
    conn = sqlite3.connect(default_sqlite3_path)
    cur = conn.cursor()
    cur.execute(''' INSERT INTO image_data (model_name, alarm_size, conf, mode, object_count, max_box_width, confidence, inference, processing_time, current_time, latitude, longitude, gpu_info, image_size) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (image_data['model_name'], image_data['alarm_size'], image_data['conf'], image_data['mode'], image_data['object_count'], image_data['max_box_width'], image_data['confidence'], image_data['inference'], image_data['processing_time'], image_data['current_time'], image_data['latitude'], image_data['longitude'], image_data['gpu_info'], image_data['image_size']))
    conn.commit()
    conn.close()

# Function to read knowledge base and extract KPIs
def get_kpis():
    g_kb = rdflib.Graph()
    #KB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KB_V3_2.n3")  # Current name of KB
    g_kb.parse(file=open(KB_path, mode="r"), format="text/n3")

    query = g_kb.query("""SELECT DISTINCT ?kpi ?value ?label
                        WHERE {
                        ?kpi a classes:KPI.
                        ?kpi rdfs:label ?label. 
                        ?kpi prop:hasValue ?value. 
                        }""")

    kpis = {}
    for row in query:
        label = str(row.asdict()['label'].toPython())
        value = float(row.asdict()['value'].toPython())  # Assuming values can be float
        kpis[label] = value
    
    return kpis



from pydantic import BaseModel
class ResponseModel(BaseModel):
    image: str
    results: dict

# Load configuration from JSON file
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

# Save configuration to JSON file
def save_config(config):
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

# Check if token is valid and return it if it is valid
def token_auth(token: str = Depends(oauth2_scheme)):
    if token != FAKE_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="📵 Invalid authorization token"
        )
    return token

# Get latest model from path
def get_latest_model(path):  # path = default_mdl_path
    list_of_files = glob.glob(f'{path}*.pt')
    if not list_of_files:
        return None  # No model found in the path
    latest_model = max(list_of_files, key=os.path.getctime)  # Get the latest model
    print(f'♻️  Latest Model: {latest_model}')
    return latest_model


# Get client IP address
@app.get("/")
async def read_root(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_host = forwarded_for.split(",")[0]
    else:
        client_host = request.client.host
    return {"📡 Client IP: ": client_host}


# About Project API
@app.get('/info')
def read_root():
    return {'Project 2023': '🔹 Potholes Detection [Moscow, 2023 г.]\n🔹 FastAPI Server with YOLOv8\n🔹 Client-Server Architecture with asynchronous requests'}


# Endpoint to update configuration from the knowledge base
@app.get("/update_config")
async def update_config():
    try:
        kpis = get_kpis()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        
        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        # Update the config with KPIs from the knowledge base
        config["Confidence"] = kpis.get("Confidence", config["Confidence"])
        config["Alarm_Size"] = kpis.get("Alarm_Size", config["Alarm_Size"])
        config["GPU_Speed"] = kpis.get("GPU_Speed", config["GPU_Speed"])

        # Write the updated configuration back to the file
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent=4)

        return {"message": "Configuration updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

 # Startup event handler
@app.on_event("startup")
async def on_startup():
    await update_config()   

# Get list of modes for Predict
@app.get("/modes")
def get_modes():
    config = load_config()  # Load actual configuration
    return {"Modes_List": config['Modes_List'], "Active_Mode": config['Active_Mode']}
    # return {"Modes_List": config['Modes_List']}

@app.post("/skyline")
def set_skyline(skyline: str):
    config = load_config()  # Load actual configuration
    if int(skyline) >= 5 or int(skyline) <= 50:
        config['Skyline'] = int(skyline)  # Set skyline
    else:
        config['Skyline'] = 28
        raise HTTPException(status_code=400, detail="Invalid skyline")
    save_config(config)
    return {"Skyline": skyline}

@app.post("/alarm_size")
def set_alarm_size(alarm_size: float):
    config = load_config()  # Load actual configuration
    if 10.0 <= alarm_size <= 500.0:
        config['Alarm_Size'] = alarm_size  # Set Alarm Size
    else:
        raise HTTPException(status_code=400, detail="Invalid Alarm Size value")
    save_config(config)  # Save Config
    return {"Alarm_Size": alarm_size}

@app.post("/confidence")
def set_confidence(confidence: float):
    config = load_config()  # Load actual configuration
    if 0.1 <= confidence <= 1.0:
        config['Confidence'] = confidence  # Set Confidence Level
    else:
        raise HTTPException(status_code=400, detail="Invalid confidence value")
    save_config(config)  # Save Config
    return {"Confidence": confidence}

# Set mode for Predict
@app.post("/modes/{mode}")
def set_mode(mode: str):
    config = load_config()  # Load actual configuration
    if mode not in config['Modes_List']:
        raise HTTPException(status_code=400, detail="Invalid mode")

    config['Active_Mode'] = mode
    save_config(config)

    return {"Active_Mode": mode}

# Get list of models for Predict
@app.get('/models')
#def list_models(token: str = Depends(token_auth)):
def list_models():
    models_dir = "models"
    models = []
    sorted_files = sorted(os.listdir(models_dir))  # Sort files in alphabetical order

    for filename in sorted_files:
        if filename.endswith(".h5") or filename.endswith(".pt"):  # Only include .h5 and .pt files in the list of models
            models.append(filename)
    #return JSONResponse(content={"Models": models})
    return {"Models": models}

@app.get("/database_summary")
async def database_summary():
    conn = sqlite3.connect(default_sqlite3_path)
    cur = conn.cursor()
    # Query for the number of records, last record's time, max confidence, and max inference
    cur.execute("""
        SELECT COUNT(*), 
               MAX(current_time), 
               MAX(max_box_width),
               MAX(confidence), 
               MAX(inference) 
        FROM image_data
    """)
    count, last_record, max_box_width, max_confidence, max_inference = cur.fetchone()
    
    conn.close()

    response = {
        "total_records": count,
        "last_record_time": last_record,
        "max_box_width": max_box_width,
        "max_confidence": max_confidence,
        "max_inference": max_inference
    }

    return response

@app.get("/download_csv")
async def download_csv():
    conn = sqlite3.connect(default_sqlite3_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM image_data ORDER BY current_time DESC LIMIT 10")
    last_10_records = cur.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    headers = ["id", "model_name", "alarm_size", "conf", "mode", "object_count", "max_box_width", "confidence", "inference", "processing_time", "current_time", "latitude", "longitude", "gpu_info", "image_size"]
    writer.writerow(headers)
    writer.writerows(last_10_records)
    output.seek(0)

    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=last_10_records.csv"})


@app.post('/predict')
#async def predict(file: UploadFile = File(...), mdl_name: Optional[str] = Form(None), token: str = Depends(token_auth)):  # Добавляем зависимость проверки токена
async def predict(file: UploadFile = File(...), mdl_name: str = Form('./default/best.pt')):
    config = load_config()         # Load actual configuration
    mkey = config['Active_Mode']   # Get Active Mode
    skyline = config['Skyline']    # Get SkyLine Level
    confidence = config['Confidence']  # Get Confidence Value
    alarm_size = config['Alarm_Size']  # Get Alarm Size Level

    if not file:
        return {"‼️ error": "🚷 No file uploaded"}

    print("... Received model name:", mdl_name)   # Print the received model name for debugging!!!
    image_stream = io.BytesIO(await file.read())  # Read the uploaded file as bytes
    f_size = image_stream.getbuffer().nbytes   # File Size
    file_size = round(f_size / 1024, 1)  # in KB
    image_stream.seek(0)  # Reset the file pointer to the beginning
    image = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), 1)  # Decode the image from bytes
    image_stream.close()  # Close the file stream

    if image is None:
        return {"‼️ error": "🚷 Invalid image file"}

    if mdl_name:
        selected_model = os.path.join(default_mdl_path, mdl_name)
        if not os.path.exists(selected_model):
            selected_model = get_latest_model(default_mdl_path)
        print(f'⚖️  Selected Model: {selected_model}')
    else:
        selected_model = get_latest_model(default_mdl_path)

    if selected_model is None:
        return {"‼️ error": "㊗️ No model files found"}

    start_time = time.time()  # Start the timer for inference time and image processing time
    if mkey == 'Basic':
        model = YOLO(selected_model) # if selected_model else None
        results = model.predict(source=image, conf=confidence)  # 0.35
        image = draw_boxes(image, results)
    elif mkey == 'Grid':
        model = YOLO(selected_model) # if selected_model else None
        results = model.predict(source=image, conf=confidence)  # 0.45
        image = draw_trapezoid_grid(image)
        image = draw_boxes(image, results)
    else:  # elif mkey == 'YOLOv8':
        #model = YOLO(selected_model) # if selected_model else None
        model = YOLO('./models//default/yolov8medium_80cls.pt')
        results = model.predict(source=image, conf=confidence)  # 0.25
        image = yolo_box(image, results)

    iH, iW = image.shape[:2]  # Image size

    is_success, buffer = cv2.imencode(".jpg", image)  # Encode the image as bytes
    if not is_success:
        return {"‼️ error": "🈲 Failed to save the image"}

    """
    # Create a file-like object from the bytes !! GOOD for sending only the Image!!
    Good practice: close the file stream after reading the bytes
    io_buf = io.BytesIO(buffer)  # Create a file-like object from the bytes
    io_buf.seek(0)  # Reset the file pointer to the beginning
    return StreamingResponse(io_buf, media_type="image/jpeg", headers={"Content-Disposition": f"inline; filename=result.jpg"})
    """

    # ++++++++++++++++++++ Process the results ++++++++++++++++++++
    max_width = 0
    max_conf = 0
    obj_count = 0
    max_speed = 0

    for result in results:
        for box in result.boxes:
            obj_count += 1
            # class_id = result.names[box.cls[0].item()]
            # speed = result.speed
            all_speed = result.speed
            speed = all_speed['inference']
            conf = box.conf[0].item()
            input_box = np.array(box.xyxy[0].tolist())
            width = input_box[2] - input_box[0]  # x2 - x1

            if width > max_width:
                max_width = round(width, 0)
                max_conf = round(conf, 2)
                max_speed = round(speed, 1)

    processing_time = round(time.time() - start_time, 2)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    latitude = round(random.uniform(-90, 90), 6)
    longitude = round(random.uniform(-180, 180), 6)
    model_name = os.path.basename(selected_model)
    gpu_info = "GeForce RTX 3090 Ti [RAM: 24 GiB]"
    image_info = f"{iW} x {iH} [{file_size} KB]"
    mode_info = f"{mkey} [{skyline} %]" if mkey == "Grid" else mkey
    if mkey == 'YOLOv8':
        model_name = 'yolov8medium_80cls.pt'

    image_data = {
        "model_name": model_name,
        "alarm_size": alarm_size,
        "conf": confidence,
        "mode": mode_info,
        "object_count": obj_count,
        "max_box_width": max_width,
        "confidence": max_conf,
        "inference": max_speed,
        "processing_time": processing_time,
        "current_time": current_time,
        "latitude": latitude,
        "longitude": longitude,
        "gpu_info": gpu_info,
        "image_size": image_info
    }
    print(f'\n{image_data}\n')

    # Insert data into the database
    if obj_count != 0 and mkey != 'YOLOv8':
        insert_image_data(image_data)

    # ++++++++++++++++++++ Image Data ++++++++++++++++++++
    # image_data = {"model_name": selected_model, "mode": mkey}
    img_str = base64.b64encode(buffer).decode()  # Encode the image as base64 string
    response_data = {
        "image": img_str,
        "results": image_data  # Extract additional data from the model
    }
    # return JSONResponse(content=json.dumps(response_data), media_type="application/json")
    response = ResponseModel(image=img_str, results=image_data)
    return response


@app.post("/predict_video")
async def predict_video(file: UploadFile = File(...), mdl_name: str = Form('./default/best.pt')):
    config = load_config()         # Load actual configuration
    confidence = config['Confidence']  # Get Confidence Value

    if mdl_name:
        selected_model = os.path.join(default_mdl_path, mdl_name)
        if not os.path.exists(selected_model):
            selected_model = get_latest_model(default_mdl_path)
        print(f'⚖️  Selected Model: {selected_model}')
    else:
        selected_model = get_latest_model(default_mdl_path)

    # Создание временного файла для видео
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_input_video_file:
        contents = await file.read()
        temp_input_video_file.write(contents)
        temp_input_video_path = temp_input_video_file.name

    # Инициализация VideoCapture
    cap = cv2.VideoCapture(temp_input_video_path)

    if not cap.isOpened():
        # Закрытие и удаление временного файла
        os.remove(temp_input_video_path)
        return {"error": "Не удалось открыть видеофайл"}

    # Получение параметров видео
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Создание временного файла для обработанного видео
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_output_video_file:
        temp_output_video_path = temp_output_video_file.name

    # Инициализация VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_video_path, fourcc, fps, (frame_width, frame_height))
    model = YOLO(selected_model)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(source=frame, conf=confidence)  # 0.35
        frame = draw_boxes(frame, results)
        out.write(frame)

    cap.release()
    out.release()
    os.remove(temp_input_video_path)

    return FileResponse(path=temp_output_video_path, filename=f"processed_{file.filename}", media_type='video/mp4')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
