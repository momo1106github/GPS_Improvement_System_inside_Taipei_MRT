# -*- coding:utf-8 -*-
import json
import csv
import noisereduce as nr
import librosa
import numpy as np
import math
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template, url_for, redirect
from flask_cors import CORS
import soundfile as sf
import os
import audioread
from pydub import AudioSegment

# from src import scene_recognition, speech_recognition
from src import MRTLocationService

frontEndDir = os.path.join( "client" , "build" )

app = Flask(__name__, static_url_path= '' , static_folder=frontEndDir)
CORS(app)

service = MRTLocationService.MRTLocationService()

@app.route('/', methods=['GET'])
def hello():
    return app.send_static_file("index.html")

@app.route('/id', methods=['GET'])
def createUser():
    return str(service.addUser())

@app.route('/audio', methods=['POST'])
def receivedAudioClip():
    print("receivedAudioClip:")
    id = request.authorization["password"]
    return service.received_audio_clip_service(id, request.files, 'wav_file')

@app.route('/image', methods=['POST'])
def receivedImage():
    print("receivedImage:")
    
    id = request.authorization["password"]
    # file = request.files['image_file']
    # file.save("./image.jpg")
    print (request.files)
    return service.received_station_image_service(id, request.files, 'image_file')

    # Todo
    # print(request.files)
    # file = request.files['image_file']
    # file.save("image.jpg")
    # result = scene_recognition.scene_recognition("image.jpg")

    # print("At Station: ", result)
    # user.state = USER_STATE["IN_STATION"] if result else USER_STATE["ON_MRT"]
    # return "OK"

@app.route('/bearing', methods=['POST'])
def receivedBearing():
    # Todo b'{"bearing":-0.6702646970416513}'
    print("request data:", request.data.decode('UTF-8'))
    bearing = json.loads(request.data.decode('UTF-8'))['bearing']
    id = request.authorization["password"]
    return service.received_user_orientation_service(id, bearing)

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=8989,ssl_context=('adhoc'))
    # app.debug = True
    # app.run()

    # heroku 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
        
