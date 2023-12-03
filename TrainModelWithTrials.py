#!/usr/bin/env python3
import threading
import os
import numpy as np
from FourInARow import FourInARowBoard  
from multiprocessing import Pool
import gc
import tensorflow as tf
import keras
import json
import copy

RED=1
BLACK=2 

def DoGameRun(model=None,rows=None,cols=None,showMoveByMove=True,showGameByGame=False,GameRecordsDir=None,gameID=0,epsilon=1.):


    fileName = None
    if GameRecordsDir is not None:
       fileName = GameRecordsDir + "/Game2" + str(gameID) + ".json"
       print(fileName)
       if os.path.exists(fileName):
           return

    print("BVL")
    boardVectorLen  = 0
    dumpFunction = FourInARowBoard.BoardInOneHotOpponentFormat
    gameVectors = []
    Features = []
    Targets = []

    gameBoard = FourInARowBoard(rows=rows,cols=cols)
    print ("Game ",gameID," Started")
 

    while not gameBoard.FourInARow() and not gameBoard.BoardFilled: 

         boardVector = dumpFunction(gameBoard)
         if boardVectorLen == 0:
             boardVectorLen = len(boardVector)
         random = np.random.default_rng(gameID)
         qnew = None

         FoundValidMove = False
         if model is not None:
           print('Random')
           randomNotQ = True if random.random() < epsilon  else False
           qinit = model.predict(np.array(boardVector).reshape(-1,boardVectorLen))[0]
           bestMoveInfo = gameBoard.FindBestMove(qinit.copy())
           qnew = bestMoveInfo["qnew"]
         else:
           randomNotQ = True
           bestMoveInfo = gameBoard.FindBestMove(np.zeros(cols))
           qnew = bestMoveInfo["qnew"]

         n = gameBoard.cols - 1
         if randomNotQ:
             while not FoundValidMove:
               action = int(random.random()*cols)
               if gameBoard.IsValidMove(action):
                 FoundValidMove = True
         else:
             sorted = np.argsort(qnew)
             while not FoundValidMove and n >= 0:
               action = sorted[n]
               if gameBoard.IsValidMove(action):
                   FoundValidMove = True
               else:
                   n -= 1

                     
         Features.append(gameBoard.BoardInOneHotOpponentFormat())
         Targets.append(qnew)
         if fileName is not None:
             gameVectors.append({"boardVector":boardVector.tolist(),"qvalues":bestMoveInfo["qnew"].tolist(),"board":gameBoard.__str__(redToken='|',noToken='.',blackToken='-')})
         gameBoard.DropPiece(action)


    if fileName is not None:
      with open(fileName,"w") as f:
        json.dump(gameVectors,f)

    if showGameByGame and not showMoveByMove:
      print (gameBoard)

    return (Features,Targets)



def GameRunBuildFiles(gameID):
    global rows,cols
    DoGameRun(model=None, rows=rows, cols=cols, showGameByGame=False, showMoveByMove=False, gameID=gameID,GameRecordsDir="Games")


def GameRunTrainModel(gameID):
    global myModel, epsilon,rows,cols
    try:
      return DoGameRun(model=myModel, rows=rows, cols=cols, showGameByGame=False, showMoveByMove=False, gameID=gameID,epsilon=epsilon)
    except Exception as e:
      print(e)





if __name__ == "__main__":
  global rows,cols
  rows=6
  cols=8
  global epsilon, myBrain

  BuildSeedFiles = False
  TrainFromModel = True

  epsilon = 1
  numGamesToPlay = 10
  myModel = tf.keras.models.load_model("OneModel.keras")

  tuples = []
  while epsilon > 0.5:
      inputs = []
      targets = []

      for i in range (0,3):
         tuples.append(GameRunTrainModel(i))
      for tuple in tuples:
        for item in tuple[0]:
          inputs.append(item)
        for item in tuple[1]:
          targets.append(item)
      inputs = np.array(inputs).reshape(-1,rows*cols*2)
      targets = np.array(targets).reshape(-1,cols)
      myModel.fit(inputs,targets,epochs=10,batch_size=100)
      print("Incremented Model")
      myModel.save("IncrementedModel.keras")
      epsilon -= (0.01)
    
