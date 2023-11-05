#!/usr/bin/env python3 import numpy as np 
import copy
import numpy as np
#
# board numpy.array(5,8) 
#  
#


RED=2 
BLACK=1 
EMPTY=0 
REDPIECE = '|'
BLACKPIECE = '-'

class FourInARowBoard():

  def __init__(self,rows=5,cols=8):
    self.board = np.zeros((rows,cols),dtype='u8')
    self.rows = rows
    self.cols = cols
    self.inarow = 4 
    self.turnColor = RED 
    self.BoardVectorLen = rows*cols*2+2

  def FindBestMove(self, qvalues):

      qvals_new = np.array(qvalues)

      for i in range(self.cols):
        if not self.IsValidMove(i):
          qvals_new[i] -= 5

      # If I can win this move, make this.
      wins = self.GoodMovesToWinThisMove()
      for i in wins:
        qvals_new[i] += 2

      stoploss = self.GoodMovesToStopALossThisMove()
      for i in stoploss:
         qvals_new[i] += 0.5

      setupwins = self.GoodMovesToSetupAWinNextMove()
      for i in setupwins:
        qvals_new[i] += 0.5 * (setupwins[i])

      setuploss = self.BadMovesThatWouldSetupALossNextMove()
      print(setuploss)
      for i in setuploss:
        qvals_new[i] -= 2

      avoidsetupfork = self.GoodMovesToAvoidSettingUpAForkNextMove()
      for i in avoidsetupfork:
        if i not in wins:
          qvals_new[i] += 1.5

      return {"qvalues": qvalues,"qnew": qvals_new, "wins": wins, "stoploss": stoploss,"setupwins": setupwins, "setuploss": setuploss,"avoidsetupfork":avoidsetupfork}


  def NextMovePiece(self):
    return REDPIECE if self.turnColor == RED else BLACKPIECE 

  def SetNextMoveColor(self,color):
    self.turnColor = RED if color == RED else BLACK

  def SetNextMoveColor(self,color):
    self.turnColor = RED if color == RED else BLACK


  # Can I win next move? 
  # Assumes game is not over. 
  def GoodMovesToWinThisMove(self, color=None):
    wins = []
    for col in range(0,self.cols):
      if self.IsValidMove(col):
        boardcopy = copy.deepcopy(self)
        if color != None:
          boardcopy.SetNextMoveColor(color)
        boardcopy.DropPiece(col)
        if boardcopy.FourInARow():
          wins.append(col)
    return wins             


  # Can I lose next move where I wouldn't have lost had I not made a move?
  # Assumes game is not over.
  #
  #
  # RRR..... case (would return 3)
  #
  def GoodMovesToStopALossThisMove(self):
     goodMovesToStopALoss = []
     for myMove in range(0,self.cols):
       boardCopy = copy.deepcopy(self)
       # If oppoent would have won anyway had I not made this move, then it doesn't count.
       if boardCopy.IsValidMove(myMove):
         if boardCopy.GoodMovesToWinThisMove(self.OpponentColor()):
            boardCopy.DropPiece(myMove)
            res = boardCopy.GoodMovesToWinThisMove()
            if not res:
               goodMovesToStopALoss.append(myMove)
     return goodMovesToStopALoss


 # Can I set up a win such that, no matter opponent's move, I still win.
  def GoodMovesToSetupAWinNextMove(self):
     setupMoves = {}
     for myFirstMove in range(0,self.cols):
       if self.IsValidMove(myFirstMove):
         CanSetupWin = False
         mostWinningMoves = 0
         for oppFirstMove in range(0,self.cols):
           boardCopy = copy.deepcopy(self)
           boardCopy.DropPiece(myFirstMove) #  Make my move
           if not boardCopy.GoodMovesToWinThisMove() and boardCopy.IsValidMove(oppFirstMove):
             boardCopy.DropPiece(oppFirstMove)
             winningMoves = boardCopy.GoodMovesToWinThisMove()
             if not boardCopy.FourInARow() and winningMoves:
               CanSetupWin = True
               mostWinningMoves = max(mostWinningMoves,len(winningMoves))
         if CanSetupWin:
           setupMoves[myFirstMove] = setupMoves.get(myFirstMove,0) + mostWinningMoves

     return setupMoves


  def BadMovesThatWouldSetupALossNextMove(self):
    #
    #    ...R
    #    ...?
    #    .RX?
    #    R?BB
    # Black's turn, X is empty. If Black places a piece at X they can set R up to win.
    #
    losssetups = []

    # Case where: I make a move, then my opponent makes a move which gives them two ways to win on their next move.
    #
    for myMove in range(0, self.cols):
      if self.IsValidMove(myMove):
        boardCopy = copy.deepcopy(self)
        # If my opponent can win next move then ingore (that is covered by CanAvoidLossNextMove())
        if boardCopy.GoodMovesToWinThisMove(color=self.OpponentColor()):
          continue
        boardCopy.DropPiece(myMove)  # My Move
        canwin = boardCopy.GoodMovesToWinThisMove()
        if len(canwin):
          losssetups.append(myMove)

    return losssetups

  def GoodMovesToAvoidSettingUpAForkNextMove(self):
      # .XRRX...  Black Placing at X blocks an 'opportunity' for Red to create a fork.
      #
      antiForkMoves = []
      for myFirstMove in range(0, self.cols):
        if self.IsValidMove(myFirstMove):
          OppCanSetupWin = False
          mostWinningMoves = 0
          boardCopy = copy.deepcopy(self)
          boardCopy.DropPiece(myFirstMove)  # Make my move
          setupOppWin = boardCopy.GoodMovesToSetupAWinNextMove()
          totalOpportunities = 0
          # Make a list of all setup moves.
          for oppMove in setupOppWin:
            if setupOppWin[oppMove] > 1:
              totalOpportunities += (setupOppWin[oppMove] -1)

          if totalOpportunities == 0:
              antiForkMoves.append(myFirstMove)

      if len(antiForkMoves) == self.cols:  # All moves equally safe, don't bias.
        return []
      return antiForkMoves

  #################################################################################################################
  #
  #
  #
  def BoardInOneHotFormat(self):
    result = [1 if self.turnColor == RED else 0, 0 if self.turnColor == RED else 1]
    for row in range(0,self.rows):
      for col in range(0,self.cols):
        if self.board[row][col] == EMPTY:
          result += [0,0]
        elif self.board[row][col] == RED:
          result += [1,0]
        elif self.board[row][col] == BLACK:
          result += [0,1]
    return np.array(result).reshape(self.BoardVectorLen) 
  
  @property
  def BoardFilled(self):
    for row in range(0,self.rows):  
      for col in range(0,self.cols):  
        if self.board[row][col] == EMPTY:
          return False 
    return True

  def CheckRight(self,row,col): 
    if col+self.inarow > self.cols:
      return False 
    if self.board[row][col] == EMPTY:
      return False 

    for i in range(1,self.inarow):
       if self.board[row][col] != self.board[row][col+i]:
         return False 
    return True

  def CheckUp(self,row,col): 
    if row+self.inarow > self.rows:
      return False
    if self.board[row][col] == EMPTY:
       return False
    for i in range(1,self.inarow):
       if (self.board[row][col] != self.board[row+i][col]):
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

  def DropPiece(self,col,color=None):
    row = 0 
    found = False
    if not self.IsValidMove(col):
       raise(Exception("Illegal Move" + str(col) + str(self)))

    if color is None:
       color = self.turnColor 
       self.turnColor = BLACK if self.turnColor == RED else RED 

    while not found and row < self.rows:
      if self.board[row][col] == EMPTY: 
        self.board[row][col] = color 
        found = True
      if not found:
        row += 1   


  def IsValidMove(self,col):
    if self.board[self.rows-1][col] == EMPTY:
      return True
    return False

  def __str__(self,redToken=REDPIECE,blackToken=BLACKPIECE,noToken=' '):
     print("RED" if self.turnColor == RED else "BLACK",end="")
     print("'s turn (",end="")
     print(redToken if self.turnColor == RED else blackToken,end=")\n")
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
  
  def TurnColor(self):
    return self.turnColor 

  def OpponentColor(self):
    return BLACK if self.turnColor == RED else RED



if __name__ == "__main__":
  nrows = 6
  ncols = 8
  d = FourInARowBoard(rows=nrows,cols=ncols) 
  d.DropPiece(0,color=RED) 
  d.DropPiece(0,color=RED) 
  d.DropPiece(0,color=RED) 
  d.DropPiece(0,color=RED) 
  d.DropPiece(1,color=BLACK) 
  d.DropPiece(2,color=BLACK) 
  d.DropPiece(3,color=BLACK) 
  d.DropPiece(4,color=BLACK) 

  assert (d.IsValidMove(0)) 
  d.DropPiece(0,color=RED) 
  assert (d.IsValidMove(0)) 
  d.DropPiece(0,color=RED) 
  assert (not d.IsValidMove(0)) 

  assert (d.CheckUp(0,0)),str(d)
  assert (not d.CheckRight(0,0))
  assert (not d.CheckUp(0,1))
  assert (d.CheckRight(0,1))


  # Test Canwin
  canwin = FourInARowBoard(rows=nrows,cols=ncols) 
  canwin.PlacePieces([(0,0)],RED) 
  assert not canwin.GoodMovesToWinThisMove()
  canwin.PlacePieces([(0,1),(0,2)],RED) 
  assert canwin.GoodMovesToWinThisMove()




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


  d = FourInARowBoard(rows=nrows,cols=ncols) 
  d.PlacePieces([(0,3),(0,4),(0,5),(0,6)],RED) 
  assert (d.CheckRight(0,3))

  d = FourInARowBoard(rows=nrows,cols=ncols) 
  d.PlacePieces([(0,4),(0,5),(0,6),(0,7)],RED) 
  assert (d.CheckRight(0,4))


  # 
  # Exporting
  # 

  d = FourInARowBoard(rows=nrows,cols=ncols) 
  d.PlacePieces([(0,0),(1,1),(2,2),(3,3)],BLACK) 
  d.PlacePieces([(3,0),(2,1),(1,2),(0,3)],RED) 

  rowlen = 2*d.cols 
  result = d.BoardInOneHotFormat()

  # Red's turn 
  assert result[0] == 1,result
  assert result[1] == 0,result

  # 0,0 Black 
  assert result[2+0] == 0,result
  assert result[2+1] == 1,result
  
  # 0,3 Red  
  assert result[2+2*3+0] == 1,result
  assert result[2+2*3+1] == 0,result
  
  # 2,0 Empty 
  assert result[2+2*rowlen+0] == 0,result
  assert result[2+2*rowlen+1] == 0,result



