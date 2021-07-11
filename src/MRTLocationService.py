from .speech_recognition import *
from .scene_recognition import *
from .color_recognition import *
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
import os
import audioread
from pydub import AudioSegment

USER_STATE = {"ON_MRT": 1, "IN_STATION": 0}

TRANSPORT_STATIONS = {
    "台北車站": ["R", "BL"], "忠孝新生": ["BL", "O"], "民權西路": ["R", "O"], "中山": ["R", "G"], "松江南京": ["O", "G"],
    "大安": ["BR", "R"], "忠孝復興": ["BR", "BL"], "南港展覽館": ["BR", "BL"], "大坪林": ["G", "Y"], "景安": ["O", "Y"], "頭前庄": ["O", "Y"],
    "古亭": ["G", "O"], "中正紀念堂": ["R", "G"], "西門": ["BL", "G"], "東門": ["O", "R"], 
    "板橋": ["BL", "Y"], "新埔": ["BL", "Y"], "新埔民生": ["BL", "Y"]
}

LINES_COLOR = { 
    "松山新店線":"G", "淡水信義線": "R", "板南線": "BL", "文湖線": "BR", "中和新蘆線": "O", "環狀線": "Y" 
}

LINES_ORIENTATIONS = {
    "文湖線": ["動物園", "木柵", "萬芳社區", "萬芳醫院", "辛亥", "麟光", "六張犁", "科技大樓", "大安", "忠孝復興", 
                "南京復興", "中山國中", "松山機場", "大直", "劍南路", "西湖", "港墘", "文德", "內湖", "大湖公園", "葫洲",
                "東湖", "南港軟體園區","南港展覽館"],
    "淡水信義線": ["象山", "台北101", "信義安和", "大安", "大安森林公園", "東門", "中正紀念堂", "台大醫院", "台北車站",
                "中山", "雙連", "民權西路", "圓山", "劍潭", "士林", "芝山", "明德", "石牌", "唭哩岸", "奇岩", "北投", 
                "新北投", "復興崗", "忠義", "關渡", "竹圍", "紅樹林", "淡水"],
    "松山新店線": ["新店", "新店區公所", "七張", "小碧潭", "大坪林", "景美", "萬隆", "公館", "台電大樓", "古亭", 
                "中正紀念堂", "小南門", "西門", "北門", "中山", "松江南京", "南京復興", "台北小巨蛋", "南京三民", "松山"],
    "中和新蘆線": ["南勢角", "景安", "永安市場", "頂溪", "古亭", "東門", "忠孝新生", "松江南京", "行天宮", "中山國小", 
                "民權西路", "大橋頭", "台北橋", "菜寮", "三重", "先嗇宮", "頭前庄", "新莊", "輔大", "丹鳳", "迴龍", 
                "三重國小", "三和國中", "徐匯中學", "三民高中", "蘆洲"],
    "板南線": ["頂埔", "永寧", "土城", "海山", "亞東醫院", "府中", "板橋", "新埔", "江子翠", "龍山寺", "西門", "台北車站",
                "善導寺", "忠孝新生", "忠孝復興", "忠孝敦化", "國父紀念館", "市政府", "永春", "後山埤", "昆陽", "南港", 
                "南港展覽館"],
    "環狀線": ["大坪林", "十四張", "秀朗橋", "景平", "景安", "中和", "橋和", "中原", "板新", "板橋", "新埔民生", "頭前庄",
                "幸福", "新北產業園區"]
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
        self.current_station = ""
        self.last_station = ""
        self.current_line = ""
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

        recognize_success = recognized_station != None
        same_station = self.user.current_station != recognized_station

        # print("83:", recognize_success, same_station, self.user.in_current_line(recognized_station), self.user)

        if recognize_success and same_station:
            self.user.location = [recognized_station["lon"], recognized_station["lat"]]
            self.user.last_station = self.user.current_station
            self.user.current_station = recognized_station["station_name_tw"]
        
        print("================")
        print("Speech Recognition Result: ")
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
        if self.user.state == USER_STATE["IN_STATION"] and self.user.current_station in TRANSPORT_STATIONS:
            color_recognition_result = color_recognition(image_file, TRANSPORT_STATIONS[self.user.current_station])
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

        pass
