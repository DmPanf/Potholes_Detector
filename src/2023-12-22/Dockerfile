# Dockerfile for YOLOv8
# Official TensorFlow GPU Jupyter
FROM tensorflow/tensorflow:latest-gpu-jupyter
#FROM nvidia/cuda:12.0.0-runtime-ubuntu22.04

# working dir
WORKDIR /yolov8

# copy all
COPY . /yolov8/

ADD https://ultralytics.com/assets/Arial.ttf /root/.config/Ultralytics/

# install
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    libgl1-mesa-glx build-essential \
    && pip install --no-cache-dir -U pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# libs
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

EXPOSE 8001

# Start FastAPI on port 8001 for 0.0.0.0 (all)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
