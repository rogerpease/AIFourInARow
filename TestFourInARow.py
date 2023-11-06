import unittest
from FourInARow import FourInARowBoard,RED,BLACK
import numpy as np

rows = 6
columns = 8
inarow=4
class MyTestCase(unittest.TestCase):

    def __init__(self,name):
        print(name)
        unittest.TestCase.__init__(self,name)
        self.rows = rows
        self.cols = columns
        self.inarow=inarow
    def test_validmove(self):

        d = FourInARowBoard(rows=self.rows, cols=self.cols)
        for i in range(0,self.rows):
            d.DropPiece(0, color=RED)
            if (i+1<self.rows):
                assert(d.IsValidMove(0))
            else:
                assert (not d.IsValidMove(0))


    def test_checkup(self):
        for row in range(0,self.rows-self.inarow+1):
            for col in range(0, self.cols):
                d = FourInARowBoard(rows=self.rows, cols=self.cols)
                d.PlacePieces([(row,col),(row+1,col),(row+2,col),(row+3,col)],color=RED)
                for checkRow in range(0, self.rows):
                   for checkCol in range(0, self.cols):
                       assert(d.FourInARow())
                       if (checkRow == row and checkCol == col):
                          assert (d.CheckUp(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)
                       else:
                          assert (not d.CheckUp(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)

    def test_checkright(self):
        for row in range(0,self.rows):
            for col in range(0, self.cols-self.inarow+1):
                d = FourInARowBoard(rows=self.rows, cols=self.cols)
                d.PlacePieces([(row,col),(row,col+1),(row,col+2),(row,col+3)],color=RED)
                for checkRow in range(0, self.rows):
                   for checkCol in range(0, self.cols):
                       assert(d.FourInARow())
                       if (checkRow == row and checkCol == col):
                          assert (d.CheckRight(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)
                       else:
                          assert (not d.CheckRight(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)

    def test_checkupright(self):
        for row in range(0,self.rows-self.inarow+1):
            for col in range(0, self.cols-self.inarow+1):
                d = FourInARowBoard(rows=self.rows, cols=self.cols)
                d.PlacePieces([(row,col),(row+1,col+1),(row+2,col+2),(row+3,col+3)],color=RED)

                for checkRow in range(0, self.rows):
                   for checkCol in range(0, self.cols):
                       assert(d.FourInARow())
                       if (checkRow == row and checkCol == col):
                          assert (d.CheckUpRight(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)
                       else:
                          assert (not d.CheckUpRight(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)
    def test_checkupleft(self):
        for row in range(0,self.rows-self.inarow+1):
            for col in range(self.inarow-1, self.cols):
                d = FourInARowBoard(rows=self.rows, cols=self.cols)
                d.PlacePieces([(row,col),(row+1,col-1),(row+2,col-2),(row+3,col-3)],color=RED)
                for checkRow in range(0, self.rows):
                   for checkCol in range(0, self.cols):
                       assert(d.FourInARow())
                       if (checkRow == row and checkCol == col):
                          assert (d.CheckUpLeft(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)
                       else:
                          assert (not d.CheckUpLeft(checkRow,checkCol)), d.__str__(redToken='|',noToken='.')+ str(checkRow) + str(checkCol)



# Test if I can win on next move
    def test_goodmovestowinthismove(self):
        # Test Canwin
        canwin = FourInARowBoard(rows=self.rows, cols=self.cols)
        canwin.PlacePieces([(0, 0)], RED)
        assert not canwin.GoodMovesToWinThisMove()
        canwin.PlacePieces([(0, 1), (0, 2)], RED)
        assert canwin.GoodMovesToWinThisMove()

    def test_howtostoplossthismove(self):
    # If red plays col3 three times and black plays col2 3 times, then red will win next move.
    #
    #                     RB
    #                     RB
    #                     RB
    # Therefore, it's an advantage to red to play 3 but it's an advantage to black (if their turn) to play.
    #  Yes, Red could win this move but we're not looking for that.
    #
        stopLossThisMove = FourInARowBoard(rows=self.rows, cols=self.cols)
        BlackCol = 2
        RedCol = 3
        stopLossThisMove.PlacePieces([(0, RedCol),(1,RedCol),(2,RedCol)], RED)
        stopLossThisMove.PlacePieces([(0, BlackCol),(1,BlackCol),(2,BlackCol)], BLACK)
        stopLossThisMove.SetNextMoveColor(RED)
        assert stopLossThisMove.GoodMovesToStopALossThisMove() == [BlackCol],stopLossThisMove.GoodMovesToStopALossThisMove()
        stopLossThisMove.SetNextMoveColor(BLACK)
        assert stopLossThisMove.GoodMovesToStopALossThisMove() == [RedCol],stopLossThisMove.GoodMovesToStopALossThisMove()


    def test_cansetupwinnextmove(self):
        # Place pieces at  .-.-......
        # If I place a piece at 2 I have 2 ways of winning next move.
        # If I place a piece at 0 or 4 I have 1 way of winning next move.
        cansetupwin = FourInARowBoard(rows=self.rows, cols=self.cols)
        cansetupwin.PlacePieces([(0, 1),(0,3)], RED)
        cansetupwin.SetNextMoveColor(RED)
        cansetup = cansetupwin.GoodMovesToSetupAWinNextMove()
        assert 2 in cansetup
        assert 0 in cansetup
        assert 4 in cansetup
        print(cansetup)
        assert cansetup[2] == 2
        assert cansetup[0] == 1
        assert cansetup[4] == 1


    def test_howtoavoidsettinguplossnextmove(self):
        #
        #    ...R
        #    ...?
        #    .RX?
        #    R?BB
        # Black's turn, X is empty if they place a piece at X they can set R up to win.
        #
        cansetuploss = FourInARowBoard(rows=self.rows, cols=self.cols)
        cansetuploss.PlacePieces([(0, 0)], RED)
        assert not cansetuploss.BadMovesThatWouldSetupALossNextMove()
        cansetuploss.PlacePieces([(0,2)], BLACK)
        cansetuploss.PlacePieces([(1, 1), (3, 3)], RED)
        cansetuploss.SetNextMoveColor(BLACK)
        #If black plays 2, they will land on 1,2. Red could play 2,2 and win.
        # However if black doesn't play 1,2 red won't be able to win.
        assert (not cansetuploss.GoodMovesToWinThisMove()),cansetuploss.GoodMovesToStopALossThisMove()
        assert (cansetuploss.BadMovesThatWouldSetupALossNextMove() == [2]),cansetuploss.BadMovesThatWouldSetupALossNextMove()

    def test_goodmovesoavoidopponentsettingupforknextmove(self):
        #
        #    .......
        #    .......
        #    .......
        #    ..RR...
        #
        #
        avoidopponentsettingupwin = FourInARowBoard(rows=self.rows, cols=self.cols)
        avoidopponentsettingupwin.PlacePieces([(0, 2),(0,3)], RED)
        avoidopponentsettingupwin.SetNextMoveColor(BLACK)
        avoidopptfork =  avoidopponentsettingupwin.GoodMovesToAvoidSettingUpAForkNextMove()
        assert len(avoidopptfork) == 2
        assert 1 in avoidopptfork,avoidopptfork
        assert 4 in avoidopptfork,avoidopptfork


    def test_findbestmove(self):
        cansetupwin = FourInARowBoard(rows=self.rows, cols=self.cols)
        cansetupwin.PlacePieces([(0,1),(0,2), (0,3)], RED)
        cansetupwin.SetNextMoveColor(RED)
        bestmoves = cansetupwin.FindBestMove(np.zeros(self.cols))
        assert 0 in bestmoves["wins"],bestmoves

    def test_baordfilled(self):
        d = FourInARowBoard(rows=self.rows, cols=self.cols)
        assert not d.BoardFilled, d.__str__()
        for row in range(self.rows):
            for col in range(int(self.cols/2)):
                d.PlacePieces([(row,col)],color=RED)
                assert not d.BoardFilled, d.__str__()
        for row in range(self.rows):
            for col in range(int(self.cols/2),self.cols):
                d.PlacePieces([(row,col)],color=RED)
        assert d.BoardFilled, d.__str__()



    def testscenarios(self):
        #  B
        #  B.....
        #  B.RR.
        stopLossThisMove = FourInARowBoard(rows=self.rows, cols=self.cols)
        stopLossThisMove.PlacePieces([(0,2), (0,3)], RED)
        BlackCol = 0
        stopLossThisMove.PlacePieces([(0, BlackCol), (1, BlackCol),(2, BlackCol)], BLACK)

        stopLossThisMove.SetNextMoveColor(RED)
        assert stopLossThisMove.GoodMovesToStopALossThisMove() == [0], stopLossThisMove.GoodMovesToStopALossThisMove()

        fiarb = FourInARowBoard.LoadBoardFromString('''........
........
........
........
-..-.|..
-.||.||-''',redToken='|',blackToken='-')
        assert(fiarb.GoodMovesToWinThisMove() == [4])


#assert (d.CheckUpRight(0, 0))
#assert (not d.CheckUpRight(nrows - 3, 0))
#assert (not d.CheckUpRight(nrows - 4, 0)), d.__str__()
#assert (d.CheckUpLeft(0, 3))
#assert (not d.CheckUpLeft(0, 2))
#assert (not d.CheckUpLeft(nrows - 3, 2))

#d = FourInARowBoard(rows=nrows, cols=ncols)
#d.PlacePieces([(0, 3), (0, 4), (0, 5), (0, 6)], RED)
#assert (d.CheckRight(0, 3))

#d = FourInARowBoard(rows=nrows, cols=ncols)
#d.PlacePieces([(0, 4), (0, 5), (0, 6), (0, 7)], RED)
#assert (d.CheckRight(0, 4))

#
# Exporting
#

#d = FourInARowBoard(rows=nrows, cols=ncols)
#d.PlacePieces([(0, 0), (1, 1), (2, 2), (3, 3)], BLACK)
#d.PlacePieces([(3, 0), (2, 1), (1, 2), (0, 3)], RED)

#rowlen = 2 * d.cols
#result = d.BoardInOneHotFormat()

# Red's turn
#assert result[0] == 1, result
#assert result[1] == 0, result

# 0,0 Black
#assert result[2 + 0] == 0, result
#assert result[2 + 1] == 1, result

# 0,3 Red
#assert result[2 + 2 * 3 + 0] == 1, result
#assert result[2 + 2 * 3 + 1] == 0, result

# 2,0 Empty
#assert result[2 + 2 * rowlen + 0] == 0, result
#assert result[2 + 2 * rowlen + 1] == 0, result

if __name__ == '__main__':
    unittest.main()
