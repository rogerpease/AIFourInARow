#!/usr/bin/env python3


import numpy as np 
from FourInARow import FourInARowBoard  
from brain import Brain

 
rows = 6 
cols = 8 
RED=1
BLACK=2 

def DoGameRuns(redModel,blackModel,rows=6,cols=8,numGamesToPlay=0):
   epsilon = 1.
   epsilonDelta = 0.0002 
   inputs = {RED: [], BLACK: []} 
   targets = {RED: [], BLACK: []} 
   lastaction  = {RED: None, BLACK: None} 
   gameCount = 0 

   while gameCount < numGamesToPlay: 
     d = FourInARowBoard(rows=6,cols=cols)
     print ("Game ",gameCount," Started") 

     gameWon = False
     boardFilled = False  
    
     while not gameWon and not boardFilled: 
 
       for color in [RED,BLACK]:
         # "Sometimes" (more often at first) pick randomly. 

         model = redModel if color == RED else blackModel 

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
         elif gameWon:
           # If I won, then punish lost side. 
           qvalues[action] = 1    
           if color == RED:
             targets[BLACK][-1][lastaction[BLACK]] = -1
           else: #  color == BLACK:
             targets[RED][-1][lastaction[RED]] = -1
         else:
           qvalues[action] *= 1.01    

         # Remembering the transition and retraining our AI
         bv = d.board.copy().reshape(-1,1,rows*cols)[0][0]
         inputs[color].append(bv) 
         targets[color].append(qvalues) 
         lastaction[color] = action
  
         print (d) 

     gameCount += 1 


   redInput  = np.array(inputs[RED]).reshape(-1,rows*cols) 
   redTarget = np.array(targets[RED]).reshape(-1,1,cols)
   redModel.fit  (redInput,redTarget, 
                  batch_size=min(40,len(inputs)))

   blackInput  = np.array(inputs[RED]).reshape(-1,rows*cols) 
   blackTarget = np.array(targets[RED]).reshape(-1,1,cols)
   blackModel.fit(blackInput,blackTarget,
                  batch_size=min(40,len(inputs)))

   if epsilon > 0:
      epsilon -= epsilonDelta 


if __name__ == "__main__":
  rows=6
  cols=8 
  redBrain = Brain(iS=(rows*cols,),outputs=cols) 
  blackBrain = Brain(iS=(rows*cols,),outputs=cols) 
  DoGameRuns(redBrain.model,blackBrain.model,rows=rows,cols=cols,numGamesToPlay=10000)
  redBrain.model.save('red_model.h5')
  blackBrain.model.save('black_model.h5')
