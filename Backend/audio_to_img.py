# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 23:17:24 2018

@author: prajw
"""

import matplotlib.pyplot as plt
plt.axis('off')
import numpy as np
import wave
import ffmpy

ff = ffmpy.FFmpeg(
executable='C:/Users/prajw/Anaconda3/envs/tensorflow/ffmpeg.win32',
inputs={"C:/Users/prajw/OneDrive/Documents/Sound recordings/rec.m4a": None},
outputs={'output.wav': None}
)
ff.run()

spf = wave.open('output.wav', 'r')
signal = spf.readframes(-1)
arr = np.fromstring(signal, int)

plt.figure(1)
#plt.title('Signal')
plt.plot(arr[:], color='#3979f0')
plt.show()
