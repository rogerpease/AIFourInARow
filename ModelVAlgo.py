#!/usr/bin/env python3


import numpy as np 
import tensorflow as tf 
from FourInARow import FourInARowBoard,RED,BLACK
from brain import Brain
 


CONVENTIONALALGO = "ConvAlgo"
AIMODEL= "AIModel"
TIE = "Tie"

def DoPlayGame(model,rows=6,cols=8,algoColor=RED):

   gameBoard = FourInARowBoard(rows=rows,cols=cols)
   print ("New Game Started") 
   playerColor=RED
   brainColor = BLACK if playerColor == RED else RED 

   gameWon = False
   boardFilled = False  


   while not gameWon and not boardFilled: 
 
     print(gameBoard.__str__(redToken='|',noToken='.',blackToken='-'))

     print(gameBoard.TurnColor(), algoColor)

     if gameBoard.TurnColor() == algoColor:
         bestMove = gameBoard.FindBestMove(np.zeros(cols))
         qvalues = bestMove["qnew"]
     else:
         vector = gameBoard.BoardInOneHotOpponentFormat()
         vector = np.array(vector).reshape(1,96)
         qvalues = model.predict(vector)

     print(qvalues)
     turn = gameBoard.TurnColor()
     gameBoard.DropPiece(np.argmax(qvalues))

     if gameBoard.FourInARow():
       if turn == algoColor:
          return CONVENTIONALALGO
       else:
          return AIMODEL

     if gameBoard.BoardFilled:
         return TIE






if __name__ == "__main__":
  rows=6
  cols=8
  algoColor = RED
  winners = {}
  loaded_model = tf.keras.saving.load_model('OneModel.keras')
  while True:
    winner = DoPlayGame(loaded_model,rows=rows,cols=cols,algoColor=algoColor)
    algoColor = RED if algoColor == BLACK else BLACK
    winners[winner] = winners.get(winner,0) + 1
    print(winners)
