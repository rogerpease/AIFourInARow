#!/usr/bin/env python3


import numpy as np 
import tensorflow as tf 
from FourInARow import FourInARowBoard  
from brain import Brain
 
RED=1
BLACK=2 

def DoPlayGame(model,rows=6,cols=8):

   d = FourInARowBoard(rows=rows,cols=cols)
   print ("New Game Started") 
   playerColor=RED
   brainColor = BLACK if playerColor == RED else RED 

   gameWon = False
   boardFilled = False  
    
   while not gameWon and not boardFilled: 
 
     print(d) 
     print("What Column?")
     action = int(input())  
     d.DropPiece(action) 

     gameWon = d.FourInARow() 
     boardFilled = d.BoardFilled 
     if not gameWon and not boardFilled: 
       vector = d.BoardInOneHotFormat()
       vector = np.array(vector).reshape(1,d.BoardVectorLen)
       qvalues = model.predict(vector)
       print(qvalues) 
       d.DropPiece(np.argmax(qvalues))

       gameWon = d.FourInARow() 
       boardFilled = d.BoardFilled 
  


if __name__ == "__main__":
  rows=6
  cols=8 
  loaded_model = tf.keras.saving.load_model('OneModel.h5')
  DoPlayGame(loaded_model,rows=rows,cols=cols)
