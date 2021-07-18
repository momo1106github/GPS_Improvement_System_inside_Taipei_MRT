FROM python:3.8.0

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && apt-get update && apt-get install -y libsndfile1 libsndfile-dev ffmpeg libsm6 libxext6 && pip install -r requirements.txt
COPY . .
CMD python App.py
