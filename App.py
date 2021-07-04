# -*- coding:utf-8 -*-

import csv
import noisereduce as nr
import librosa
from scipy.io import wavfile
import speech_recognition as sr
import numpy as np
import math
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template, url_for, redirect
from flask_cors import CORS
import soundfile as sf
import os
import audioread
from pydub import AudioSegment
from src import scene_recognition

def get_station_info(filename):

    station_list = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            station_list.append(row)
            
    return station_list

USER_STATE = {"ON_MRT": 1, "IN_STATION": 0}
STATION_INFO = get_station_info('./station_info.csv')


class User:
    def __init__(self):
        self.location = [0, 0]
        self.orientation = 0
        self.state = USER_STATE["ON_MRT"]
        self.current_station = ""
        self.last_station = ""
        self.time_since_last_station = 0
        self.audio_cnt = 0
        self.audios = []
        self.videos = []
        self.oris = []
    
    def add_audio(self, audio):
        while (len(self.audios) >= 5):
            self.audios.pop(0)
        self.audios.append(audio)



# def noise_reduction(in_file):
#     data, rate = librosa.load(in_file)
#     noisy_part = data[0:15000] # To sutdy 
#     reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=False)
#     out_file = "./output/" + in_file[:-4] + "__noise_reduced.wav"
#     # print (reduced_noise)
#     # Convert `data` to 32 bit integers:
#     reduced_noise = (np.iinfo(np.int32).max * (reduced_noise/np.abs(reduced_noise).max())).astype(np.int32)
#     # print (reduced_noise)
#     wavfile.write(out_file, rate, reduced_noise)
#     return out_file

def broadcast_recognition(in_file):
    return True
    
def speech_recognition(user, audio_clip):
    user.add_audio(audio_clip)

    r = sr.Recognizer()
    MRT = sr.AudioFile(audio_clip)
    
    with MRT as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    
    result = []
    # only recognizes chinese
    try:
        result = r.recognize_google(audio, language='zh-TW')
    except:
        return None
    
    try:
        alterResult = r.recognize_google(audio, show_all=True, language='zh-TW')
        print("alterResult:", alterResult)
    except:
        print("Alter result failed")

    print("bestResult: ", result)
    output = None
    for station in STATION_INFO:
        if str(result).find(station['station_name_tw']) != -1:
            # print(f'station name:{station['station_name_tw']}')
            output = station
    
    # out_file = "./output/" + in_file[:-4] + "__speech_recognized.wav"
    # with open(out_file, 'w') as f:
    #     f.write(str(output))
    return output
    
def station_recognition(user, audio_clip):
    print ("audio_clip: ", audio_clip)

    # noise_reduced_file = noise_reduction(input_file)

    # if broadcast_recognition(noise_reduced_file) == False:
    #     exit(0)
    recognized_station = speech_recognition(user, audio_clip)

    print(recognized_station) 
    return recognized_station 

def received_audio_clip_service(user, audio_file):
    recognized_station = station_recognition(user, audio_file)
    if (recognized_station != None and user.current_station != recognized_station):
        user.location = [recognized_station["lon"], recognized_station["lat"]]
        user.last_station = user.current_station
        user.current_station = recognized_station["station_name_tw"]
    
    print ("user location: ", user.location)
    return jsonify(user.location)
    
frontEndDir = os.path.join( "client" , "build" )

app = Flask(__name__, static_url_path= '' , static_folder=frontEndDir)
CORS(app)
# app.config["DEBUG"] = True
# app.run()

user = User()


@app.route('/', methods=['GET'])
def hello():
    # with open('./index.html', newline='', encoding="utf-8") as webPage:
    #     buffer = webPage.read()
    # return buffer
    return app.send_static_file("index.html")

@app.route('/orientation', methods=['POST'])
def receivedOrintation():
    # orientation = request.body.orientation
    pass

@app.route('/audio', methods=['POST'])
def receivedAudioClip():
    out_file = "./output/out.wav"
    print(request.files, request.files['wav_file'])
    file = request.files['wav_file']
    file.save(out_file)
    
    try:
    # sf.write('./tmp.wav', file, 16000)
        data, rate = librosa.load(out_file)
        file = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
        wavfile.write("./output/out.wav", rate, file) # rate: 44100 
        print("done sending")
        return received_audio_clip_service(user, "./output/out.wav")
    except:

        with audioread.audio_open(out_file) as f:
            print(f.channels, f.samplerate, f.duration)
            rate = f.samplerate
            for buf in f:
                data = buf

                file = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
                wavfile.write("./output/out.wav", rate, file) # rate: 44100 
                print("done sending")
                return received_audio_clip_service(user, "./output/out.wav")

@app.route('/image', methods=['POST'])
def receivedImage():
    # Todo
    print(request.files)
    file = request.files['image_file']
    file.save("image.jpg")
    result = scene_recognition.scene_recognition("image.jpg")

    print("result: ", result)

    return "OK"

@app.route('/bearing', methods=['POST'])
def receivedBearing():
    # Todo
    print(request.data.bearing)

    return "OK"
if __name__ == '__main__':
    app.run()
        