from scipy.io import wavfile
import csv
import noisereduce as nr
import librosa
import numpy as np
import math
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template, url_for, redirect
from flask_cors import CORS
import soundfile as sf
from pydub import AudioSegment

from .speech_recognition import *
from .scene_recognition import *
from .color_recognition import *
from .stations_info import TRANSPORT_STATIONS, LINES_COLOR, STATION_LINES

USER_STATE = {"ON_MRT": 1, "IN_STATION": 0}

STATION_LINE_ORIENTATIONS = {"動物園": [{"orientation": 0, "line": "文湖線", "direction": 1}, {"orientation": 180, "line": "文湖線", "direction": -1}],
                             "大安": [{"orientation": 0, "line": "文湖線", "direction": 1}, {"orientation": 180, "line": "文湖線", "direction": -1}, 
                                     {"orientation": 0, "line": "淡水信義線", "direction": 1}, {"orientation": 180, "line": "淡水信義線", "direction": -1}],
                             "木柵": [{"orientation": 0, "line": "文湖線", "direction": 1}, {"orientation": 180, "line": "文湖線", "direction": -1}],
                             "忠孝復興": [{"orientation": 0, "line": "文湖線", "direction": 1}, {"orientation": 180, "line": "文湖線", "direction": -1}, 
                                     {"orientation": 0, "line": "板南線", "direction": 1}, {"orientation": 180, "line": "板南線", "direction": -1}],
                             }

def get_station_info(filename):

    station_list = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            station_list.append(row)
            
    return station_list

class User:
    def __init__(self):
        self.location = [0, 0]
        self.orientation = 0
        self.state = USER_STATE["ON_MRT"]
        self.current_station = {}
        self.last_station = {}
        self.current_line = ""
        self.line_direction = 1
        self.time_since_last_station = 0
        # self.audio_cnt = 0
        # self.audios = []
        # self.videos = []
        # self.oris = []
    
    # def add_audio(self, audio):
    #     while (len(self.audios) >= 5):
    #         self.audios.pop(0)
    #     self.audios.append(audio)

    def in_current_line(self, recognized_station):
        return self.current_line != "" and self.current_line in TRANSPORT_STATIONS[recognized_station.line_name]

class MRTLocationService:
    def __init__(self):
        self.user = User()
        self.stations_info = get_station_info('./station_info.csv')
        
    
    def received_audio_clip_service(self, files, file_key):
        if self.user.state == USER_STATE["IN_STATION"]:
            print("User in station, no Speech Recognition Service")
            return jsonify(self.user.location)

        audio_file = "./output/out.wav"
        file = files[file_key]
        file.save(audio_file)

        data, rate = librosa.load(audio_file)
        file = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
        wavfile.write(audio_file, rate, file)

        recognized_station = speech_recognition(self.user, audio_file, self.stations_info)

        # print("83:", recognize_success, same_station, self.user.in_current_line(recognized_station), self.user)

        if recognized_station:
            self.user.location = [recognized_station["lon"], recognized_station["lat"]]
            self.user.last_station = self.user.current_station
            self.user.current_station = recognized_station
            if recognized_station["station_name_tw"] not in TRANSPORT_STATIONS:
                self.user.current_line = LINES_COLOR[recognized_station["line_name"]]
            else:
                self.user.current_line = LINES_COLOR[self.user.last_station["line_name"]] if self.user.last_station else ""
                
        print("================")
        print("Speech Recognition Result: ")
        if recognized_station:
            print("recognized station: ", recognized_station["station_name_tw"]) 
        print("user location: ", self.user.location)
        if self.user.state == 0:
            print("user state: In Station")
        else:
            print("user state: On MRT")
        print("user station_line_color: ", self.user.current_line)
        print("================")

        return jsonify(self.user.location)

    def received_station_image_service(self, files, file_key):
        image_file = "./output/image.jpg"
        file = files[file_key]
        file.save(image_file)

        color_recognition(image_file, ["BL", "G"])
        
        
        scene_recognition_result = scene_recognition(image_file)
        self.user.state = USER_STATE["IN_STATION"] if scene_recognition_result else USER_STATE["ON_MRT"]
        print("IN Station: ", scene_recognition_result)
        color_recognition_result = None
        if self.user.state == USER_STATE["IN_STATION"] and self.user.current_station["station_name_tw"] in TRANSPORT_STATIONS:
            color_recognition_result = color_recognition(image_file, TRANSPORT_STATIONS[self.user.current_station["station_name_tw"]])
            self.user.current_line = color_recognition_result[0]        
            print("Dominant Color: ", color_recognition_result)
        
        print("================")
        print("Scene Recognition Result: ")
        if self.user.state == USER_STATE["IN_STATION"]:
            print("Dominant Color: ", color_recognition_result)
        print ("user location: ", self.user.location)
        if self.user.state == 0:
            print ("user state: In Station")
        else:
            print ("user state: On MRT")
        print ("user station_line_color: ", self.user.current_line)
        print("================")
        return jsonify(self.user.location)
    

    def received_user_orientation_service(self, orientation):
        print("received", orientation)
        if self.user.state == USER_STATE["ON_MRT"]:
            pass
        
        orientations = STATION_LINE_ORIENTATIONS["動物園"]
        orientation = int(orientation + 180) % 360


        print("before orientation:", self.user.line_direction, " ", self.user.current_line)

        for ori in orientations:
            bound = [( ori["orientation"] - 60 + 360 ) % 360, ( ori["orientation"] + 60 + 360 ) % 360]
            if bound[0] <= orientation <= bound[1] and self.user.current_line == LINES_COLOR[ori["line"]]:
                self.user.line_direction = ori["direction"]
                break        
                
        print("oriented user:", self.user.line_direction, " ", self.user.current_line)
        return jsonify(self.user.location)