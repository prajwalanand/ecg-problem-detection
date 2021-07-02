# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:06:13 2018

@author: prajw
"""

import cv2
import os

dirs = ['Final_Data/healthy/', 'Final_Data/arrhythmia/', 'Final_Data/ischemia/', 'Final_Data/heart_attack/']

for dir in dirs:
    for root, d, files in os.walk(dir):
        for f in files:
            img_gray_mode = cv2.imread(dir+f, 0)
            cv2.imwrite('Grey_Images/'+dir.split('/')[1]+'/'+f, img_gray_mode)