#!/usr/bin/env python3 

import numpy as np 

#
# board numpy.array(5,8) 
#  
#

RED=2 
BLACK=1 
EMPTY=0 

class FourInARowBoard():

  def __init__(self,rows=5,cols=8):
    self.board = np.zeros((rows,cols),dtype='u8')
    self.rows = rows
    self.cols = cols
    self.inarow = 4 
    
  @property
  def BoardFilled(self):
    for row in range(0,self.rows):  
      for col in range(0,self.cols):  
        if self.board[row][col] == EMPTY:
          return False 
    return True

  def CheckRight(self,row,col): 
    if col+self.inarow >= self.cols:
      return False 
    if self.board[row][col] == EMPTY:
      return False 

    for i in range(1,self.inarow):
       if self.board[row][col] != self.board[row][col+i]:
         return False 
    return True

  def CheckUp(self,row,col): 
    if row+self.inarow >= self.rows:
      return False 
    for i in range(1,self.inarow):
       if self.board[row][col] != self.board[row+i][col]:
         return False 
    return True

  def CheckUpRight(self,row,col): 
    if self.board[row][col] == EMPTY:
      return False 
    if row+self.inarow > self.rows or col+self.inarow > self.cols:
      return False 
    for i in range(1,self.inarow):
       if self.board[row][col] != self.board[row+i][col+i]:
         return False 
    return True

  def CheckUpLeft(self,row,col): 
    if self.board[row][col] == EMPTY:
      return False 
    if row+self.inarow > self.rows or col-self.inarow+1 < 0:
      return False 
    for i in range(1,self.inarow):
       if self.board[row][col] != self.board[row+i][col-i]:
         return False 
    return True


  def FourInARow(self): 
    for row in range(0,self.rows):  
      for col in range(0,self.cols):  
        if ((self.board[row][col] != EMPTY) and 
            ((self.CheckRight(row,col))  or         
             (self.CheckUp(row,col))     or 
             (self.CheckUpLeft(row,col)) or          
             (self.CheckUpRight(row,col)))): 
          return True   
    return False 

  def DropPiece(self,col,color):
    row = 0 
    found = False
    while not found and row < self.rows:
      if self.board[row][col] == 0: 
        self.board[row][col] = color 
        found = True
      if not found:
        row += 1   
    if not found: 
      self.DropPiece((col+1)%self.cols,color)

  def __str__(self,redToken='|',blackToken='-',noToken=' '):
     result = "" 
     for row in reversed(range(0,self.rows)): 
       for col in range(0,self.cols): 
         result += redToken if self.board[row][col] == RED else blackToken if self.board[row][col] == BLACK else noToken if self.board[row][col] == EMPTY else '?'
       result += "\n"   
     result += "FourInARow: "+str(self.FourInARow())+"\n"   
     result += "BoardFilled: "+str(self.BoardFilled)+"\n"   
     return result
  
  def PlacePieces(self,locs,color):
    for loc in locs:
      self.board[loc[0]][loc[1]] = color

 
if __name__ == "__main__":
  nrows = 6
  ncols = 8
  d = FourInARowBoard(rows=nrows,cols=ncols) 
  d.DropPiece(0,RED) 
  d.DropPiece(0,RED) 
  d.DropPiece(0,RED) 
  d.DropPiece(0,RED) 
  d.DropPiece(1,BLACK) 
  d.DropPiece(2,BLACK) 
  d.DropPiece(3,BLACK) 
  d.DropPiece(4,BLACK) 

  assert (d.CheckUp(0,0))
  assert (not d.CheckRight(0,0))
  assert (not d.CheckUp(0,1))
  assert (d.CheckRight(0,1))

  print(d) 

  d = FourInARowBoard(rows=nrows,cols=ncols) 

  assert not d.BoardFilled, d.__str__() 
 
  d.PlacePieces([(0,0),(1,1),(2,2),(3,3)],BLACK) 
  d.PlacePieces([(3,0),(2,1),(1,2),(0,3)],RED) 

  assert (d.CheckUpRight(0,0))
  assert (not d.CheckUpRight(nrows-3,0))
  assert (not d.CheckUpRight(nrows-4,0)),d.__str__()
  assert (d.CheckUpLeft(0,3))
  assert (not d.CheckUpLeft(0,2))
  assert (not d.CheckUpLeft(nrows-3,2))

  print(d) 

