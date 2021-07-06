# -*- coding:utf-8 -*-

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

@app.route('/orientation', methods=['POST'])
def receivedOrintation():
    # orientation = request.body.orientation
    # Add Color recognition
    pass

@app.route('/audio', methods=['POST'])
def receivedAudioClip():
    print("receivedAudioClip:")
    return service.received_audio_clip_service(request.files, 'wav_file')


    # if user.state = USER_STATE["IN_STATION"]:
    #     return "Not in MRT"
    
    # out_file = "./output/out.wav"
    # print(request.files, request.files['wav_file'])
    # file = request.files['wav_file']
    # file.save(out_file)
    
    # # try:
    # # sf.write('./tmp.wav', file, 16000)
    # data, rate = librosa.load(out_file)
    # file = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    # wavfile.write("./output/out.wav", rate, file) # rate: 44100 
    # print("done sending")
    # return speech_recognition.received_audio_clip_service(user, "./output/out.wav", STATIONS_INFO)
    # except:

    #     with audioread.audio_open(out_file) as f:
    #         print(f.channels, f.samplerate, f.duration)
    #         rate = f.samplerate
    #         for buf in f:
    #             data = buf

    #             file = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    #             wavfile.write("./output/out.wav", rate, file) # rate: 44100 
    #             print("done sending")
    #             return speech_recognition.received_audio_clip_service(user, "./output/out.wav")

@app.route('/image', methods=['POST'])
def receivedImage():
    print("receivedImage:")
    
    # file = request.files['image_file']
    # file.save("./image.jpg")
    print (request.files)
    return service.received_station_image_service(request.files, 'image_file')

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
    # Todo
    print("received bearing: ", request.data.bearing)
    return service.received_user_orientation_service(request.data.bearing)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8989,ssl_context=('adhoc'))
    # app.debug = True
    # app.run()
        
