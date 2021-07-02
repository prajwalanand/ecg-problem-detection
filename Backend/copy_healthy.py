# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 10:09:00 2018

@author: prajw
"""

import os
import random
from shutil import copyfile

files = []

for root, dirs, fil in os.walk('imgs/healthy/'):
    files = fil

subset_files = random.sample(files, 5000)

for f in subset_files:
    copyfile('imgs/healthy/'+f, 'Final_Data/healthy/'+f)