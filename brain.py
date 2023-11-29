#!/usr/bin/env python3 

import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Conv2D,MaxPooling2D, Flatten
from keras.optimizers import Adam
import tensorflow as tf 


physical_devices = tf.config.experimental.list_physical_devices('GPU')
assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
config = tf.config.experimental.set_memory_growth(physical_devices[0], True)

class Brain():
  def __init__(self, iS = None,outputs=1,lr=0.0001):
    self.learningRate = lr 
    self.inputShape = iS 
    self.model = Sequential() 
    self.model.add(Dense(units=400,input_shape=iS))
    self.model.add(Dense(units=100))
    self.model.add(Dense(units=100))
    self.model.add(Dense(units=100))
    self.model.add(Dense(units=100))
    self.model.add(Dense(units=outputs))
    self.model.compile(loss='mse',optimizer=Adam(learning_rate=self.learningRate))
  
  def loadModel(self,filepath):
    self.model = load_model(filepath)
    return self.model

if __name__ == "__main__":
  samples = 100000
  d = Brain(iS=(4,),lr=0.01,outputs=1)
  fs = np.array(np.random.randn(4*samples)*1000).reshape(samples,4)
  #fs = np.array(range(4*samples)).reshape(samples,4)
  labels = np.array([[x[0]+4*x[1] + x[2] + 2*x[3]] for x in fs]).reshape(samples,1)
  print (fs,labels) 
  d.model.fit(fs,labels,epochs=5,batch_size=1000)
  p = d.model.predict([[10, 20, 30, 40]])
  assert(p[0] > 190 and p[0] < 210)
  p = d.model.predict([[80, 60, 40, 10]])
  assert (p[0] > 370 and p[0] < 390)
