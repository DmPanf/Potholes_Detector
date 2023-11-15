from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import io
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Optional
from pydantic import BaseModel
import glob
import os
#import torch
#torch.cuda.is_available = lambda : False  # принудительно использовать только CPU для PyTorch
from bboxes import draw_boxes


default_mdl_path = './models/'  # Путь по умолчанию, где хранятся модели
# Токен авторизации для примера. В реальном приложении это должно быть защищено!
FAKE_TOKEN = "goodroad"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(title="Potholes Detection System API", version="0.1.0", debug=True)  # Инициализация FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def token_auth(token: str = Depends(oauth2_scheme)):
    if token != FAKE_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="📵 Неверный токен авторизации"
        )
    return token

def get_latest_model(path):  # Функция для выбора самой последней модели
    list_of_files = glob.glob(f'{path}*.pt')
    if not list_of_files:
        return None  # Ни одного файла модели не найдено
    latest_model = max(list_of_files, key=os.path.getctime)  # Выбираем самый свежий файл
    print(f'♻️  Latest Model: {latest_model}')
    return latest_model


# Добавление статических файлов
#app.mount('/static', StaticFiles(directory="static"), name="static")
#templates = Jinja2Templates(directory="templates")


#@app.get("/", response_class=HTMLResponse)
#async def read_root(request: Request):
#    ## return templates.TemplateResponse("index.html", {"request": request})
#    #model_files_response = list_models()
#    #model_files = model_files_response.body  # Вытащить содержимое JSONResponse
#    #model_files_dict = json.loads(model_files.decode())  # Декодировать и конвертировать в словарь
#    model_files = list_models()  # это словарь
#    print(f"\n🛒 Доступные модели: {model_files['Models']}")
#    return templates.TemplateResponse("index.html", {"request": request, "models": model_files['Models']})


@app.get("/")
async def read_root(request: Request):
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_host = forwarded_for.split(",")[0]
    else:
        client_host = request.client.host
    return {"📡 Client IP: ": client_host}


@app.get('/info')
def read_root():
    return {'Project 2023': 'Pothole Detection [Moscow, 2023 г.]'}


@app.get('/models')
def list_models(token: str = Depends(token_auth)):
    models_dir = "models"
    models = []

    sorted_files = sorted(os.listdir(models_dir))

    for filename in sorted_files:
        if filename.endswith(".h5") or filename.endswith(".pt"):  # Расширения файлов моделей
            models.append(filename)
    #return JSONResponse(content={"Models": models})
    return {"Models": models}


@app.post('/predict')
#async def predict(file: UploadFile = File(...), mdl_name: Optional[str] = Form(None), token: str = Depends(token_auth)):  # Добавляем зависимость проверки токена
#async def predict(file: UploadFile = File(...), mdl_name: Optional[str] = Form(None)):
async def predict(file: UploadFile = File(...), mdl_name: str = Form('./default/best.pt')):
    print("... Received model name:", mdl_name) # для отладки !!!
    image_stream = io.BytesIO(await file.read())
    image_stream.seek(0)
    image = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), 1)
    image_stream.close()

    if image is None:
        return {"error": "Invalid image file"}

    # Если имя модели предоставлено, создаем полный путь к модели
    if mdl_name:
        selected_model = os.path.join(default_mdl_path, mdl_name)
        # Проверяем, существует ли файл модели
        if not os.path.exists(selected_model):
            selected_model = get_latest_model(default_mdl_path)
        print(f'⚖️  Selected Model: {selected_model}')
    else:
        selected_model = get_latest_model(default_mdl_path)

    if selected_model is None:
        return {"error": "No model files found"}

    # Загружаем модель в память
    model = YOLO(selected_model) # if selected_model else None
    results = model.predict(source=image, conf=0.35, )
    image = draw_boxes(image, results)

    is_success, buffer = cv2.imencode(".jpg", image)
    if not is_success:
        return {"error": "Failed to save the image"}

    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)
    return StreamingResponse(io_buf, media_type="image/jpeg", headers={"Content-Disposition": f"inline; filename=result.jpg"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
