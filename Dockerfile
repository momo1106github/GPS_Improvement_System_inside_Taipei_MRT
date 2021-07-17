FROM python:3.8.0

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip && apt-get update && apt-get install -y libsndfile1 libsndfile-dev ffmpeg libsm6 libxext6 && pip install -r requirements.txt

EXPOSE 8989

CMD python App.py