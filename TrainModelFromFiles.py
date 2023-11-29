#!/usr/bin/env python3

import os
import numpy as np 
from FourInARow import FourInARowBoard  
from brain import Brain
from SampleQueue import SampleQueue 
import gc
import tensorflow as tf
import keras
import json
import copy 
rows = 6 
cols = 8 
RED=1
BLACK=2 

REDPIECE = '|'
BLACKPIECE = '-'

DEFINITE = 1
HOPELESS = 2
UNCERTAIN = 0
DEFINITENO = -1



if __name__ == "__main__":
  rows=6
  cols=8 
  myBrain = Brain(iS=(rows*cols*2,),outputs=cols,lr=0.001)
  gameCount = 0
  numGamesToPlay = 1000
  gameFound = True
  Inputs = [] 
  Targets = []
  for root, dirs, files in os.walk("Games"):
    for file in files:
      if ".json" in file:
       try:
        with open("Games/"+file) as f:
          data = json.loads("\n".join(f.readlines()))
          for item in data[6:]: 
            Inputs.append(item['boardVector'])
            Targets.append(item['qvalues'])
       except Exception as e:
        print(str(e))

  print (len(Inputs),len(Targets))
  Inputs  = np.array(Inputs).reshape(-1,rows*cols*2)
  Targets = np.array(Targets).reshape(-1,cols)
  myBrain.model.fit(Inputs,Targets,epochs=5,batch_size=2000)
  gc.collect()
  myBrain.model.save('OneModel.keras')

