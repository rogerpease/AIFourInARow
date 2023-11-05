#!/usr/bin/env python3


import numpy as np 
from FourInARow import FourInARowBoard  
from brain import Brain
from SampleQueue import SampleQueue 
import gc
import tensorflow as tf
import keras 
 
rows = 6 
cols = 8 
RED=1
BLACK=2 

def DoGameRuns(redModel,blackModel,rows=rows,cols=cols,numGamesToPlay=0,showMoveByMove=False,showGameByGame=False):
  redSQ   = SampleQueue(max_memory=100) 
  blackSQ = SampleQueue(max_memory=100) 
  epsilon = 1.
  epsilonDelta = 0.0002 

  priorSideAction = None 
  gameCount = 0 

  dumpFunction = FourInARowBoard.BoardInOneHotFormat

  while gameCount < numGamesToPlay: 
    d = FourInARowBoard(rows=rows,cols=cols)
    print ("Game ",gameCount," Started") 
  
 
    gameWon = False
    boardFilled = False  
   
    color = RED 
    while not gameWon and not boardFilled: 

         # "Sometimes" (more often at first) pick randomly. 
         if gameWon or boardFilled: 
           continue 

         model = redModel if color == RED else blackModel 
         sampleQueue      = redSQ   if color == RED else blackSQ  
         otherSampleQueue = blackSQ if color == RED else redSQ  

         boardVector = dumpFunction(d)
         boardVector = np.array(boardVector).reshape(-1,rows*cols*3)
         qvalues = model.predict(boardVector)[0]
         gc.collect()
         keras.backend.clear_session()

         if np.random.rand(1) < epsilon:  
           action = int(np.random.rand()*cols)
         else:  
           action = np.argmax(qvalues)

         d.DropPiece(action,color) 

         gameWon = d.FourInARow() 
         boardFilled = d.BoardFilled 
  
         if not gameWon and boardFilled:
           qvalues[action] = -1    
           sampleQueue.remember(boardVector,qvalues) 

         elif gameWon:
           # If I won, then punish lost side. 
           for i in range(0,cols):
             qvalues[i] = 0    
           qvalues[action] = 1    
           sampleQueue.remember(boardVector,qvalues) 

         else:
           qvalues[action] *= 1.01    
           sampleQueue.remember(boardVector,qvalues) 

         color = RED if color == BLACK else BLACK 
 
         if showMoveByMove:  
           print (d) 

    if showGameByGame:  
      print (d) 

    gameCount += 1 

    redInput, redTarget  = redSQ.get_batch()
    redInput  = np.array(redInput).reshape(-1,144)
    redTarget = np.array(redTarget).reshape(-1,8)

    redModel.fit(redInput,redTarget)

    blackInput,  blackTarget = blackSQ.get_batch() 
    blackInput  = np.array(blackInput).reshape(-1,144)
    blackTarget = np.array(blackTarget).reshape(-1,8)
    blackModel.fit(blackInput,blackTarget)
    gc.collect()
 
    if epsilon > 0:
       epsilon -= epsilonDelta 


if __name__ == "__main__":
  rows=6
  cols=8 
  redBrain = Brain(iS=(rows*cols*3,),outputs=cols) 
  blackBrain = Brain(iS=(rows*cols*3,),outputs=cols) 
  DoGameRuns(redBrain.model,blackBrain.model,rows=rows,cols=cols,numGamesToPlay=10000,showGameByGame=True)
  redBrain.model.save('red_model.h5')
  blackBrain.model.save('black_model.h5')
