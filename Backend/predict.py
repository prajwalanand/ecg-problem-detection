import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model

img_width, img_height = 32, 32
model_path = './models/model.h5'
model_weights_path = './models/weights.h5'
model = load_model(model_path)
model.load_weights(model_weights_path)
outfile = 'labels.txt'

def predict(file):
  x = load_img(file, target_size=(img_width,img_height))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = model.predict(x)
  result = array[0]
  print("Predicted answer: ", result)
  return result

with open(outfile, 'w') as op:
	for i, ret in enumerate(os.walk('./test-data/text')):
	  for i, filename in enumerate(ret[2]):
		if filename.startswith("."):
		  continue
		print("Label: ")
		result = predict(ret[0] + '/' + filename)
		op.write(filename+','+result)