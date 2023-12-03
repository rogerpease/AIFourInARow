#!/usr/bin/env python3
#
#
#
#

import numpy as np
from FourInARow import BestMoves

class QComputer():
    def __init__(self):
        pass


    @staticmethod
    def ComputeBestMove(cols,bestMoves):

        if bestMoves.goodMovesToWin:
            return np.random.choice(bestMoves.goodMovesToWin)
        elif bestMoves.goodMovesToStopLoss:
            return np.random.choice(bestMoves.goodMovesToStopLoss)
        elif bestMoves.goodMovesToSetupWins:
            return np.random.choice(list(bestMoves.goodMovesToSetupWins.keys()))
        elif bestMoves.badMovesToSetupLoss:
            return np.random.choice(bestMoves.badMovesToSetupLoss)
        elif bestMoves.goodMovesToAvoidSetupFork:
            return np.random.choice(bestMoves.goodMovesToAvoidSetupFork)
        else:
            # Best move that isn't in illegal moves
            validMoves = [i for i in range(0,cols)  if i not in bestMoves.illegalMoves]
            return np.random.choice(validMoves)

    @staticmethod
    def ComputeNewQ(oldQ,bestMoves):
        newQ = np.array(oldQ)
        for i in range(0,len(oldQ)):
            if i in bestMoves.illegalMoves:
                newQ[i] = -1
            elif i in bestMoves.goodMovesToWin:
                newQ[i] = 1
            elif i in bestMoves.goodMovesToStopLoss:
                newQ[i] = 0.3
            elif i in bestMoves.goodMovesToSetupWins:
                newQ[i] = 0.4
            elif i in bestMoves.badMovesToSetupLoss:
                newQ[i] = -1
            elif i in bestMoves.goodMovesToAvoidSetupFork:
                newQ[i] = 1
            else:
                newQ[i] = 0

def SelfTest():
    bm = BestMoves(goodMovesToWin=[0],goodMovesToStopLoss=[1],goodMovesToSetupWins=[2],badMovesToSetupLoss=[3],goodMovesToAvoidSetupFork=[4])
    q = QComputer()

    assert 0 in bm.goodMovesToWin
    assert 1 in bm.goodMovesToStopLoss
    assert 2 in bm.goodMovesToSetupWins
    assert 3 in bm.badMovesToSetupLoss
    assert 4 in bm.goodMovesToAvoidSetupFork
    bestmove = q.ComputeBestMove(5,bm)
    assert bestmove == 0, bestmove


if __name__ == "__main__":
    SelfTest()
    print("OK")