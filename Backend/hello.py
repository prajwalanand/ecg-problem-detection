# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 12:33:12 2018

@author: prajw
"""

from flask import Flask, request
from flask_cors import CORS
from record import record
from test_cnn import predict
from history import get_files
app = Flask(__name__)
CORS(app)

@app.route("/")
def rec():
    #print(request.args)
    req_type = request.args.get("type")
    user = request.args.get("user")
    if req_type == "record":
        record(user)
        return "Recording done"
    elif req_type == 'test':
        return predict(user)
    elif req_type == 'history':
        return get_files(user)
    elif req_type == 'test_hist':
        return predict(user, user)

if __name__ == "__main__":
    app.run()