#!/usr/bin/env python3 

import numpy as np
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Conv2D,MaxPooling2D, Flatten
from keras.optimizers import Adam

class Brain():
  def __init__(self, iS = None,outputs=1,lr=0.01):
    self.learningRate = lr 
    self.inputShape = iS 
    self.model = Sequential() 
    self.model.add(Dense(units=250,activation='relu',input_shape=iS))
    self.model.add(Dense(units=outputs))
    self.model.compile(loss='mean_squared_error',optimizer=Adam(learning_rate=self.learningRate)) 
  
  def loadModel(self,filepath):
    self.model = load_model(filepath)
    return self.model

if __name__ == "__main__": 
  d = Brain(iS=(1,4),lr=0.1,outputs=1)
  fs = np.array(range(0,1000)).reshape(250,-1,4) 
  labels = np.array([[x[0][0]+x[0][1] + x[0][2] + x[0][3]] for x in fs]).reshape(250,1,1)
  print (fs,labels) 
  d.model.fit(fs,labels,epochs=25,batch_size=10) 
  p = d.model.predict([[[10, 20, 30, 40]]])
  print(p)
