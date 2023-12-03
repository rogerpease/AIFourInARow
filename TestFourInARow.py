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


    def test_getwinlists(self):
        d = FourInARowBoard(rows=6, cols=8)
        winlists = d.GetWinLists((4,4))
        expectList = [
            # UpRight
            [(1, 1), (2, 2), (3, 3), (4, 4)],
            [(2, 2), (3, 3), (4, 4), (5, 5)],
            # UpLeft  4,4 5,3 3,5 2,6
            [(2,6),(3,5),(4,4),(5,3)],
            [(1,7),(2,6),(3,5),(4,4)],

            # Up
            [(1, 4), (2, 4), (3, 4), (4, 4)],
            [(2, 4), (3, 4), (4, 4), (5, 4)],

            # Horiz
            [(4, 1), (4, 2), (4, 3), (4, 4)],
            [(4, 2), (4, 3), (4, 4), (4, 5)],
            [(4, 3), (4, 4), (4, 5), (4, 6)],
            [(4, 4), (4, 5), (4, 6), (4, 7)]

        ]
        for expected in expectList:
            assert expected in winlists, str(expected) + str(winlists)
        assert len(winlists) == len(expectList), winlists

        winlists = d.GetWinLists((2,2))
        expectList = [
            # UpRight
            [(1, 1), (2, 2), (3, 3), (4, 4)],
            [(0, 0), (1, 1), (2, 2), (3, 3)],
            [(2, 2), (3, 3), (4, 4),(5,5)],


            # UpLeft  4,4 5,3 3,5 2,6
            [(0,4),(1,3),(2,2),(3,1)],
            [(1, 3), (2, 2), (3, 1), (4, 0)],

            # Up
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 2), (2, 2), (3, 2), (4, 2)],
            [(2, 2), (3, 2), (4, 2), (5,2)],

            # Horiz
            [(2,0),(2,1),(2,2),(2,3)],
            [(2,1),(2,2),(2,3),(2,4)],
            [(2,2),(2,3),(2,4),(2,5)]

        ]

        for expected in expectList:
          assert expected in winlists, str(expected) + str(winlists)
        assert len(winlists) == len(expectList), winlists


    def test_fourinarow(self):
        d = FourInARowBoard(rows=self.rows, cols=self.cols)
        d.PlacePieces([(0, 0), (0, 1), (0, 2)], RED)
        assert not d.FourInARow()
        d.PlacePieces([(3, 3)], RED)
        assert not d.FourInARow()
        d.PlacePieces([(0, 3)], RED)
        assert d.FourInARow()

    # Test if I can win on next move
    def test_goodmovestowinthismove(self):
        # Test Canwin
        canwin = FourInARowBoard(rows=self.rows, cols=self.cols)
        canwin.PlacePieces([(0, 2)], RED)
        assert not canwin.GoodMovesToWinThisMove()
        canwin.PlacePieces([(0, 1), (0, 3)], RED)
        assert canwin.GoodMovesToWinThisMove()
        assert len(canwin.GoodMovesToWinThisMove()) == 2
        assert 0 in canwin.GoodMovesToWinThisMove(),canwin.GoodMovesToWinThisMove()
        assert 4 in canwin.GoodMovesToWinThisMove(),canwin.GoodMovesToWinThisMove()

    def test_goodmovestostopalossthismove(self):
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
        assert 0 in bestmoves["goodmovestowin"], bestmoves
        assert 4 in bestmoves["goodmovestowin"], bestmoves

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




if __name__ == '__main__':
    unittest.main()
