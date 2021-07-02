# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 12:18:58 2018

@author: prajw
"""

import os

def get_files(user):
    file_list= [x.split('.')[0] for x in os.listdir('files/') if user in x]
    return ';'.join(file_list)