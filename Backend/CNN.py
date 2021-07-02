# -*- coding: utf-8 -*-
"""
@author: prajw
"""

import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from keras.layers.core import Activation
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from keras.utils import to_categorical
from keras.models import load_model
from sklearn import svm
import cv2
import os
import pickle

mode = 'test'#'train'
final_layer = 'dense'#'svm'

class LeNet:
	@staticmethod
	def build(width, height, depth, classes):

		model = Sequential()
		inputShape = (height, width, depth)
 
		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)

		model.add(Conv2D(20, (5, 5), padding="same",
			input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(Conv2D(50, (5, 5), padding="same"))
		model.add(Activation("relu"))
		model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

		model.add(Flatten())
		model.add(Dense(500))
		model.add(Activation("relu"))
 
		model.add(Dense(classes))
		model.add(Activation("softmax"))
 
		return model

EPOCHS = 25
INIT_LR = 1e-3
BS = 32

data = []
labels = []

imagePaths = ['Grey_Images/healthy/', 'Grey_Images/arrhythmia/', 'Grey_Images/ischemia/', 'Grey_Images/heart_attack/']
print('Loading Images')
for imagePath in imagePaths:
   for f in os.listdir(imagePath):
    	image = cv2.imread(imagePath+f, 0)
    	image = cv2.resize(image, (28, 28))
    	image = img_to_array(image)
    	data.append(image)
     
    	label = imagePaths.index(imagePath)
    	labels.append(label)

data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25)

if final_layer == 'dense':
    trainY = to_categorical(trainY, num_classes=4)
    testY = to_categorical(testY, num_classes=4)

if mode == 'train':
    
    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                             horizontal_flip=True, fill_mode="nearest")

    print('Compiling Model')
    model = LeNet.build(width=28, height=28, depth=1, classes=4)
    print(model.summary())
    opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
    model.compile(loss="categorical_crossentropy", optimizer=opt,
    	metrics=["categorical_accuracy"])
    
    print('Training Model')
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
    	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
    	epochs=EPOCHS, verbose=1)
    
    model.save('ecg.model')


elif mode == 'test':
    
    model = load_model('ecg.model')
    
    if final_layer == 'dense':
        score = model.evaluate(testX, testY, batch_size=BS, verbose=1)
    
    elif final_layer == 'svm':
        model.pop()
        model.pop()
        model.pop()
        model.pop()
        
        print(model.summary())
        
        test_image = 'Grey_Images/heart_attack/img974.png'
        image = cv2.imread(test_image, 0)
        orig = image.copy()
         
        image = cv2.resize(image, (28, 28))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        
        print(model.predict(image))
        
        svm_trainX = []
        svm_testX = []
        for trn_image in trainX:
            svm_trainX.append(model.predict(np.expand_dims(trn_image, axis=0))[0])
        for tst_image in testX:
            svm_testX.append(model.predict(np.expand_dims(tst_image, axis=0))[0])
        
        svc = svm.SVC(decision_function_shape='ovo')
        
        svc.fit(svm_trainX, trainY)
        
        with open('svm.pkl', 'wb') as modfile:
            pickle.dump(svc, modfile)
        
        preds = []
        for tst in svm_testX:
            preds.append(svc.predict(tst.reshape(1, -1))[0])
        
        count = sum([preds[i] == testY[i] for i in range(len(preds))])
        
        score = count/len(preds)
    
    print(score)