# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 22:49:48 2018

@author: prajw
"""
import wfdb
import os
import matplotlib.pyplot as plt
plt.ioff()

def ptbdb():
    pass

for root, dirs, files in os.walk("Data"):
    for dir in dirs:
        if dir == 'staffiii':
            d = 'staffiii/data'
        elif dir != 'ptbdb':
            d = dir
        else:
            ptbdb()
        for root2, dirs2, files2 in os.walk("Data/"+d):
            ecg_files = list(set([x.split('.')[0] for x in files2 if all([x.split('.')[0]+y in files2 for y in ('.hea', '.atr', '.dat')])]))
            for f in ecg_files:
                print(f)
                record = wfdb.rdrecord("Data/"+d+"/"+f)
                sig = record.p_signal
                