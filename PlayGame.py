#!/usr/bin/env python3
#
#

import time
import numpy as np
from QComputer import QComputer
from FourInARow import FourInARowBoard,BestMoves


RED=1
BLACK=2


class Player():
    class PlayerType:
        Human = 0
        Algo = 1
        Model = 2
    def __init__(self,color,playerType,model=None):
        self.playerType = playerType
        self.color = color
        if playerType == Player.PlayerType.Model:
          self.model = model

    def ComputeMove(self,board):
      if self.playerType == Player.PlayerType.Human:
        print(board)
        print("What Column?")
        s = int(input())
        return {"move":s}
      elif self.playerType == Player.PlayerType.Algo:
        bestmoves = board.FindBestMove()
        return {"move":QComputer.ComputeBestMove(board.cols,bestmoves),"bestmoves":bestmoves}
      elif self.playerType == Player.PlayerType.Model:
        vector = board.BoardInOneHotOpponentFormat()
        vector = np.array(vector).reshape(1,96)
        qvalues = self.model.predict(vector)
        return {"move":np.argmax(qvalues)}



def DoPlayGame(board,redPlayer,blackPlayer,transcriptFileName=None):

   print ("New Game Started")
   playerColor=RED
   transcript = []

   done = False
   while not done:
     player = redPlayer if playerColor == RED else blackPlayer



     action = player.ComputeMove(board)
     board.DropPiece(action["move"])
     if transcriptFileName:
        transcript.append({"boardVector": boardVector,"bestmoves": action["bestmoves"]})


     if board.FourInARowFound:
       print(board)
       if playerColor == RED:
         print("Red Wins")
       else:
         print("Black Wins")
       done = True
     elif board.BoardFilled:
       print("Draw")
       done = True
     playerColor = BLACK if playerColor == RED else RED


   if transcriptFileName:
        import json
        with open(transcriptFileName, 'w') as outfile:
            for move in transcript:
                for bestmove in move["bestmoves"]:
                    if isinstance(bestmove,np.ndarray):
                        bestmove = bestmove.tolist()
            json.dump(transcript, outfile, indent=4)


def SetupAndPlayGame(rows=6,cols=8,redPlayer=None,blackPlayer=None,transcriptFileName=None):
  board = FourInARowBoard(rows=rows, cols=cols)
  if redPlayer is None:
    redPlayer = Player(Player.PlayerType.Algo,RED)
  if blackPlayer is None:
    blackPlayer = Player(Player.PlayerType.Algo,BLACK)
  DoPlayGame(board,redPlayer,blackPlayer,transcriptFileName=transcriptFileName)

if __name__ == "__main__":

  import argparse
  parser = argparse.ArgumentParser(description="Play against AI. Play")
  parser.add_argument("--rows", default=6, type=int)
  parser.add_argument("--cols", default=8, type=int)
  parser.add_argument("--redPlayer",   default=Player.PlayerType.Algo,choices = [Player.PlayerType.Human,Player.PlayerType.Algo,Player.PlayerType.Model],help="Player Type Algo = 1, Human = 0, Model = 2", type=int)
  parser.add_argument("--blackPlayer", default=Player.PlayerType.Algo,choices = [Player.PlayerType.Human,Player.PlayerType.Algo,Player.PlayerType.Model],help="Player Type Algo = 1, Human = 0, Model = 2", type=int)
  parser.add_argument("--transcriptFile",  default=None,type=str)
  args = parser.parse_args()



  startTime = time.time()
  redPlayer = Player(playerType=args.blackPlayer,color=RED)
  blackPlayer = Player(playerType=args.redPlayer,color=BLACK)
  SetupAndPlayGame(rows=args.rows,cols=args.cols,redPlayer=redPlayer,blackPlayer=blackPlayer,transcriptFileName=args.transcriptFile)
  print (time.time() - startTime)