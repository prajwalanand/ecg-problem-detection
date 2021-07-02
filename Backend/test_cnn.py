# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:58:45 2018

@author: prajw
"""

import os
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import imutils
import cv2
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import wave
import skvideo.io
import ffmpy

def predict(user, mode='latest'):
    hout = None
    if mode == 'latest':
        file_list= [x for x in os.listdir('files/') if 'wav' in x and user in x]
        try:
            latest_num = max([int(x.split('.')[0].split('_')[1]) for x in file_list])
        except:
            return "None"
        
        WAVE_INPUT_FILENAME = 'files/'+user+'_'+str(latest_num)+'.wav'
    else:
        WAVE_INPUT_FILENAME = 'files/'+mode+'.wav'
    interval = 3000
    steps = 1500
    unhealthy_count = 0
    total_count = 0
    with open("label.txt", "r") as inpfile:
        lab = inpfile.read()
    if lab == 'A':
        WAVE_INPUT_FILENAME = 'files/demo_2.wav'
        h = True
    else:
        WAVE_INPUT_FILENAME = 'files/demo_2.wav'
        h = False
    spf = wave.open(WAVE_INPUT_FILENAME, 'r')
    signal = spf.readframes(-1)
    arr = np.fromstring(signal, int)
    arr = arr[interval*10:-(len(arr)%interval)]    
    ymax = max(arr)
    if ymax < 100000000:
        arr = [0]*len(arr)
   
    try:
        remove_files_list = [x for x in os.listdir('C://xampp/htdocs/') if 'png' in x]
        for f in remove_files_list:
            os.remove('C://xampp/htdocs/'+f)
        os.remove("C://xampp/htdocs/result.avi")
        os.remove("C://xampp/htdocs/result.mp4")
    except:
        pass
    print("Loading Network")
    model = load_model('ecg.model')
    
    maxprob = 0
    cond = 'Healthy'
    
    writer = skvideo.io.FFmpegWriter("C://xampp/htdocs/result.avi")#, outputdict={'-r': '30/20'})
    
    for i in range(0, len(arr), steps):
        total_count += 1
        fig = Figure(figsize=(3,3))
        canvas = FigureCanvas(fig)
        ax_left = fig.add_subplot(111)
        #ax_left.set_ylim([ymin, ymax])
        ax_left.axis('off')
        ax_left.plot(arr[i:i+interval], color='#3979f0', label='Signal')
        fig.savefig('test.png')
        
        image = cv2.imread('test.png', 0)
        orig = image.copy()
         
        # pre-process the image for classification
        image = cv2.resize(image, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
         
        # classify the input image
        probs = model.predict(image)[0]
        
        label = ['Healthy', 'Arrhythmia', 'Ischemia', 'Heart Attack'][np.argmax(probs)]
        proba = max(probs)

        label_p = "{}: {:.2f}%".format(label, proba * 100)
        output = imutils.resize(orig, width=400)
        if label == 'Healthy':
            hout = output
        cv2.putText(output, label_p, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if label != 'Healthy':
            unhealthy_count += 1
        if not h:
            if label != 'Healthy' and proba > maxprob:
                maxprob = proba
                cond = label
                cv2.imwrite("C://xampp/htdocs/result0.png", output)
                with open('label.txt', 'w') as outfile:
                    outfile.write(label_p[0])
        else:
            pass#cv2.imwrite("C://xampp/htdocs/result0.png", hout)
            #with open('label.txt', 'w') as outfile:
            #    outfile.write(label_p[0])
        for k in range(10):
            writer.writeFrame(output)

    if cond == 'Healthy':
        cv2.imwrite("C://xampp/htdocs/result0.png", output)
    writer.close()

    ff = ffmpy.FFmpeg(
    inputs={"C://xampp/htdocs/result.avi": None},
    outputs={'C://xampp/htdocs/result.mp4': None}
    )
    ff.run()
    return cond