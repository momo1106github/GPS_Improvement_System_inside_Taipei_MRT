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
    
def speech_recognition(user, audio_clip, stations_info):
    # user.add_audio(audio_clip)


    r = sr.Recognizer()
    MRT = sr.AudioFile(audio_clip)
    
    with MRT as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    
    result = []
    alter_results = []
    # only recognizes chinese
    try:
        result = r.recognize_google(audio, language='zh-TW')
    except:
        return None
    
    try:
        alter_results = r.recognize_google(audio, show_all=True, language='zh-TW')
        print("alterResult:", alter_results)
    except:
        print("Alter result failed")

    print("bestResult: ", result)
    output = None
    
    for station in stations_info:
        if str(result).find(station['station_name_tw']) != -1:
            output = station
            break
        for alter_result in alter_results:
            if str(alter_result).find(station['station_name_tw']) != -1:
                # print(f'station name:{station['station_name_tw']}')
                output = station
    
    # out_file = "./output/" + in_file[:-4] + "__speech_recognized.wav"
    # with open(out_file, 'w') as f:
    #     f.write(str(output))
    print("Best output: ", output)
    return output
    
def station_recognition(user, audio_clip):
    print ("audio_clip: ", audio_clip)

    # noise_reduced_file = noise_reduction(input_file)

    # if broadcast_recognition(noise_reduced_file) == False:
    #     exit(0)
    recognized_station = speech_recognition(user, audio_clip)

    print(recognized_station) 
    return recognized_station

