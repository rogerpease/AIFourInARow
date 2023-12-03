#!/usr/bin/env python3 

import copy
import numpy as np


RED=2 
BLACK=1 
EMPTY=0 
REDPIECE = '|'
BLACKPIECE = '-'


class BestMoves(object):
    def __init__(self, goodMovesToWin=[], goodMovesToStopLoss=[], goodMovesToSetupWins=[], badMovesToSetupLoss=[],
                 goodMovesToAvoidSetupFork=[], illegalMoves=[]):
        self.goodMovesToWin = goodMovesToWin
        self.goodMovesToStopLoss = goodMovesToStopLoss
        self.goodMovesToSetupWins = goodMovesToSetupWins
        self.badMovesToSetupLoss = badMovesToSetupLoss
        self.goodMovesToAvoidSetupFork = goodMovesToAvoidSetupFork
        self.illegalMoves = illegalMoves


class FourInARowBoard():

  def __init__(self,rows=6,cols=8,inarow=4):
    self.board = np.zeros((rows,cols),dtype='u8')
    self.rows = rows
    self.cols = cols
    self.inarow = inarow
    self.pieceList = {}
    self.pieceList[RED] = []
    self.pieceList[BLACK] = []
    self.turnColor = RED
    self.FourInARowFound = False


  def FindBestMove(self):
      illegalMoves = []
      for i in range (0,self.cols):
        if not self.IsValidMove(i):
          illegalMoves.append(i)

      # If I can win this move, make this.
      wins = self.GoodMovesToWinThisMove()
      stoploss = self.GoodMovesToStopALossThisMove()
      setupwins = self.GoodMovesToSetupAWinNextMove()
      setuploss = self.BadMovesThatWouldSetupALossNextMove()
      avoidsetupfork = self.GoodMovesToAvoidSettingUpAForkNextMove()
      return BestMoves(goodMovesToWin=wins,goodMovesToStopLoss=stoploss,goodMovesToSetupWins=setupwins,badMovesToSetupLoss=setuploss,goodMovesToAvoidSetupFork=avoidsetupfork,illegalMoves=illegalMoves)


  def NextMovePiece(self):
    return REDPIECE if self.turnColor == RED else BLACKPIECE 

  def SetNextMoveColor(self,color):
    self.turnColor = RED if color == RED else BLACK

  def SetNextMoveColor(self,color):
    self.turnColor = RED if color == RED else BLACK


  # Can I win next move? 
  # Assumes game is not over. 
  def GoodMovesToWinThisMove(self, color=None):
    winmoves = []
    if color is None:
      color = self.turnColor
    for col in range(0,self.cols):
      if self.IsValidMove(col):
        row = self._RowDroppedPieceWouldLandOn(col)
        winlists =  self.GetWinLists((row,col))
        for winlist in winlists:
           winlist.remove((row,col))
           if self.ColorContainsAllPieces(color,winlist):
               winmoves.append(col)
    return winmoves


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
         if boardCopy.GoodMovesToWinThisMove(color=self.OpponentColor()):
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


  def BoardInOneHotOpponentFormat(self):
    result = []

    for row in range(0,self.rows):
      for col in range(0,self.cols):
        if self.board[row][col] == EMPTY:
          result += [0,0]
        elif self.board[row][col] == self.turnColor:
          result += [1,0]
        elif self.board[row][col] == self.OpponentColor():
          result += [0,1]
    return np.array(result).reshape(2*self.rows*self.cols)
  
  @property
  def BoardFilled(self):
    if len(self.pieceList[RED]) + len(self.pieceList[BLACK]) == self.rows*self.cols:
      return True
    return False


  def ContainsInvalidLocatione(self,listOflocations):
    for i in listOflocations:
      if i[0] < 0 or i[0] >= self.rows or i[1] < 0 or i[1] >= self.cols:
        return True
    return False


  # if you are checking at 4,4  you could win with:
  #   - Horiz: 1,0 - 1,3   1,1 -1,4 1,2-1,5, etc.
  #   - Vert:  0,1 1,1 2,1 3,1
  #   - Diag:  0,0 1,1 2,2 3,3  1,1 2,2 3,3,4,4
  #   - Diag:  0,4 1,3 2,2 3,1

  def GetWinLists(self,loc):
    row,col = loc
    result = []
    # Horizontal
    for sdist in range(0,self.inarow):
        sublist = []
        for num in range(0,self.inarow):
          sublist.append((row, col -sdist + num))
        if not self.ContainsInvalidLocatione(sublist):
          result.append(sublist)
    # Vertical
    for sdist in range(0, self.inarow):
        sublist = []
        for num in range(0, self.inarow):
            sublist.append((row -sdist + num, col))
        if not self.ContainsInvalidLocatione(sublist):
            result.append(sublist)
    # Up-Left
    for sdist  in range(0,self.inarow):
        sublist = []
        for num in range(0, self.inarow):
           sublist.append((row + num-sdist, col-num +sdist))
        if not self.ContainsInvalidLocatione(sublist):
            result.append(sublist)

    # Up-Right
    for sdist  in range(0,self.inarow):
        sublist = []
        for num in range(0, self.inarow):
            sublist.append((row + num-sdist, col+num -sdist))
        if not self.ContainsInvalidLocatione(sublist):
            result.append(sublist)

    return result

  def ColorContainsAllPieces(self,color, listOflocations):
    for location in listOflocations:
       if location not in self.pieceList[color]:
            return False
    return True

  def FourInARow(self):
    for color in (RED,BLACK):
       for piece in self.pieceList[color]:
           winList = self.GetWinLists(piece)
           for set in winList:
             if self.ColorContainsAllPieces(color,set):
               return True

    return False 


  def _RowDroppedPieceWouldLandOn(self,col):
      row = 0
      found = False
      while not found and row < self.rows:
          if self.board[row][col] == EMPTY:
              return row
          row += 1


  def DropPiece(self,col,color=None):
      if not self.IsValidMove(col):
          raise (Exception("Illegal Move" + str(col) + str(self)))
      row = self._RowDroppedPieceWouldLandOn(col)
      if color == None:
          color = self.turnColor
      self.board[row][col] = color
      self.pieceList[color].append((row,col))
      self.turnColor = self.OpponentColor()
      winList = self.GetWinLists((row,col))
      for set in winList:
          if self.ColorContainsAllPieces(color, set):
              self.FourInARowFound = True

  @staticmethod
  def LoadBoardFromString(boardString,blackToken=BLACKPIECE,redToken=REDPIECE):
   # RB...._BR...
    result = FourInARowBoard()
    rowStrings = boardString.split("\n")
    rowStrings = [x.strip() for x in rowStrings if len(x.strip()) > 0]
    numRows = len(rowStrings)
    numCols = len(rowStrings[0])

    result = FourInARowBoard(rows=numRows, cols=numCols)

    row = numRows
    for rowString in rowStrings:
       rowString = rowString.strip()
       row -= 1
       for col in range(0,result.cols):
         if rowString[col] == redToken:
           result.board[row][col] = RED
         elif rowString[col] == blackToken:
           result.board[row][col] = BLACK
         elif rowString[col] == '.':
           result.board[row][col] = EMPTY
         else:
           raise(Exception("Illegal Move" + str(rowString) + " Col " + str(col)))
    assert (row == 0)
    return result


  def IsValidMove(self,col):
    if self.board[self.rows-1][col] == EMPTY:
      return True
    return False

  def __str__(self,redToken=REDPIECE,blackToken=BLACKPIECE,noToken=' ',lineBreak="\n"):
     result = ""
     result = ""
     result +=  "RED" if self.turnColor == RED else "BLACK"
     result += "'s turn ("
     result += redToken if self.turnColor == RED else blackToken
     result += ")"
     result += lineBreak

     for row in reversed(range(0,self.rows)): 
       for col in range(0,self.cols): 
         result += redToken if self.board[row][col] == RED else blackToken if self.board[row][col] == BLACK else noToken if self.board[row][col] == EMPTY else '?'
       result += lineBreak
     result += "FourInARow: "+str(self.FourInARow())+lineBreak
     result += "BoardFilled: "+str(self.BoardFilled)+lineBreak
     return result
  
  def PlacePieces(self,locs,color):
    for loc in locs:
      self.board[loc[0]][loc[1]] = color
      self.pieceList[color].append(loc)
  
  def TurnColor(self):
    return self.turnColor 

  def OpponentColor(self):
    return BLACK if self.turnColor == RED else RED

