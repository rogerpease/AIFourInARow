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

     result = d.FindBestMove(np.zeros(cols))
     print('Your best move is ',result)

     print("What Column?")
     action = int(input())  
     d.DropPiece(action) 

     gameWon = d.FourInARow() 
     boardFilled = d.BoardFilled 
     if not gameWon and not boardFilled: 
   
       result = d.FindBestMove(np.zeros(cols))
       print(result) 
       print ("Program says its best move is ",np.argmax(result["qnew"]))
       d.DropPiece(np.argmax(result["qnew"]))

       gameWon = d.FourInARow() 
       boardFilled = d.BoardFilled 
  


if __name__ == "__main__":
  rows=6
  cols=8 
  loaded_model = tf.keras.saving.load_model('OneModel.h5')
  print (loaded_model.inputs)
  DoPlayGame(loaded_model,rows=rows,cols=cols)
