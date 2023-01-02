#!/usr/bin/env python3


import numpy as np 
from FourInARow import FourInARowBoard  
from brain import Brain
 
RED=1
BLACK=2 

def DoPlayGame(model,rows=6,cols=8):

   d = FourInARowBoard(rows=6,cols=cols)
   print ("New Game Started") 
   playerColor=RED
   brainColor = BLACK if playerColor == RED else RED 

   gameWon = False
   boardFilled = False  
    
   while not gameWon and not boardFilled: 
 
     print("What Column?")
     action = int(input())  
     d.DropPiece(action,playerColor) 

     print(d) 
     gameWon = d.FourInARow() 
     boardFilled = d.BoardFilled 
     if not gameWon and not boardFilled: 
       qvalues = model.predict(d.board.reshape(1,1,rows*cols)[0])[0]
       d.DropPiece(np.argmax(qvalues),brainColor)
       gameWon = d.FourInARow() 
       boardFilled = d.BoardFilled 
  
     print(d) 


if __name__ == "__main__":
  rows=6
  cols=8 
  brain = Brain(iS=(1,48))
  brain.loadModel('red_model.h5')
  DoPlayGame(brain.model,rows=rows,cols=cols)
