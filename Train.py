#!/usr/bin/env python3


import numpy as np 
from FourInARow import FourInARowBoard  
from brain import Brain
from SampleQueue import SampleQueue 

 
rows = 6 
cols = 8 
RED=1
BLACK=2 

def DoGameRuns(redModel,blackModel,rows=6,cols=8,numGamesToPlay=0,showMoveByMove=False,showGameByGame=False):
  redSQ =SampleQueue(max_memory=100) 
  blackSQ =SampleQueue(max_memory=100) 
  epsilon = 1.
  epsilonDelta = 0.0002 

  priorSideAction = None 
  gameCount = 0 

  while gameCount < numGamesToPlay: 
    d = FourInARowBoard(rows=6,cols=cols)
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

         qvalues = model.predict(d.board.reshape(1,1,rows*cols)[0])[0]

         if np.random.rand(1) < epsilon:  
           action = int(np.random.rand()*cols)
         else:  
           action = np.argmax(qvalues)

         d.DropPiece(action,color) 

         gameWon = d.FourInARow() 
         boardFilled = d.BoardFilled 
  
         if not gameWon and boardFilled:
           qvalues[action] = -1    
           sampleQueue.remember(d.board.reshape(1,1,rows*cols),qvalues) 
         elif gameWon:
           # If I won, then punish lost side. 
           qvalues[action] = 1    
           sampleQueue.remember(d.board.reshape(1,1,rows*cols),qvalues) 
           inputs,outputs = otherSampleQueue.getlast()  
           outputs[prevaction] = -1 
           otherSampleQueue.updatelast(inputs,outputs)  

         else:
           qvalues[action] *= 1.01    
           sampleQueue.remember(d.board.reshape(1,1,rows*cols),qvalues) 

         prevaction = action 
         color = RED if color == BLACK else BLACK 
 
         if showMoveByMove:  
           print (d) 

    if showGameByGame:  
     print (d) 
    gameCount += 1 

    redInput, redTarget  = redSQ.get_batch()
    redModel.fit  (redInput,redTarget, batch_size=min(40,len(inputs)))
 
    blackInput,  blackTarget = blackSQ.get_batch() 
    blackModel.fit(blackInput,blackTarget, batch_size=min(40,len(inputs)))
 
    if epsilon > 0:
       epsilon -= epsilonDelta 


if __name__ == "__main__":
  rows=6
  cols=8 
  redBrain = Brain(iS=(rows*cols,),outputs=cols) 
  blackBrain = Brain(iS=(rows*cols,),outputs=cols) 
  DoGameRuns(redBrain.model,blackBrain.model,rows=rows,cols=cols,numGamesToPlay=10000,showGameByGame=True)
  redBrain.model.save('red_model.h5')
  blackBrain.model.save('black_model.h5')
