# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 12:43:42 2018

@author: prajw
"""

import pyaudio
import os
import wave
#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.ioff()

def record(user, duration=10):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = duration
    file_list= [x for x in os.listdir('files/') if 'wav' in x and user in x]
    try:
        latest_num = max([int(x.split('.')[0].split('_')[1]) for x in file_list])
    except:
        latest_num = 0
    
    WAVE_OUTPUT_FILENAME = 'files/'+user+'_'+str(latest_num+1)+'.wav'
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print("* recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

