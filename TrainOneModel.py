#!/usr/bin/env python3


import numpy as np 
from FourInARow import FourInARowBoard  
from brain import Brain
from SampleQueue import SampleQueue 
import gc
import tensorflow as tf
import keras 
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




def DoGameRuns(model,rows=rows,cols=cols,numGamesToPlay=0,showMoveByMove=True,showGameByGame=False):
  sampleQueue = SampleQueue(max_memory=100) 
  epsilon = 1.
  epsilonDelta = 0.0002 

  priorSideAction = None 
  gameCount = 0 

  dumpFunction = FourInARowBoard.BoardInOneHotFormat

  while gameCount < numGamesToPlay: 
    gameBoard = FourInARowBoard(rows=rows,cols=cols)
    print ("Game ",gameCount," Started") 
 
    gameWon = False
    boardFilled = False  
   
    while not gameBoard.FourInARow() and not gameBoard.BoardFilled: 

         boardVector = dumpFunction(gameBoard)
         qvalues = model.predict(np.array(boardVector).reshape(-1,gameBoard.BoardVectorLen))[0]
         gc.collect()
         keras.backend.clear_session()
         print ("Provided qvalues",qvalues)

         # Go through each possible move, see if it wins. If so, 
         bestMoveInfo = gameBoard.FindBestMove(qvalues)
         print("New qvalues", bestMoveInfo)
         sampleQueue.remember(boardVector,bestMoveInfo["qnew"])

         FoundValidMove = False
         randomNotQ = True if np.random.rand(1) < epsilon  else False

         n = gameBoard.cols-1
         sorted = np.argsort(qvalues)
             
         while not FoundValidMove and n >= 0:
           if randomNotQ:
             action = int(np.random.rand()*cols)
             if gameBoard.IsValidMove(action):
                FoundValidMove = True 
             else: 
                print("Rejected "+str(action) + " pos " +str(n))
           else:  
             action = sorted[n]
             if gameBoard.IsValidMove(action):
                FoundValidMove = True

             else: 
                print("Rejected "+str(action) + " pos " +str(n))
                n -= 1 

         if showMoveByMove:
           print (gameBoard)
           print("Dropping piece at   ",action)

         gameBoard.DropPiece(action) 




    if showGameByGame:  
      print (gameBoard) 

    gameCount += 1 

    if (gameCount % 10) == 0:
      Input, Target = sampleQueue.get_batch(batch_size=100)
      Input  = np.array(Input).reshape(-1,gameBoard.BoardVectorLen)
      Target = np.array(Target).reshape(-1,gameBoard.cols)
      model.fit(Input,Target)
      gc.collect()
      sampleQueue = SampleQueue(max_memory=100)

    if epsilon > 0:
       epsilon -= epsilonDelta 

    if (gameCount %10 == 0):
      myBrain.model.save('OneModel.h5')


if __name__ == "__main__":
  rows=6
  cols=8 
  myBrain = Brain(iS=(2+rows*cols*2,),outputs=cols) 
  DoGameRuns(myBrain.model,rows=rows,cols=cols,numGamesToPlay=10000,showGameByGame=True,showMoveByMove=True)
  myBrain.model.save('OneModel.h5')
