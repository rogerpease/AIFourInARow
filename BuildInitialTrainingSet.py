#!/usr/bin/env python3
import threading
import os
import numpy as np

import QComputer
from FourInARow import FourInARowBoard  
from multiprocessing import Pool
import gc
import tensorflow as tf
import keras
import json
import copy

from PlayGame import SetupAndPlayGame


def GameRunBuildFiles(gameID):
    global rows,cols
    redPlayer = Player(playerType=args.blackPlayer, color=RED)
    blackPlayer = Player(playerType=args.redPlayer, color=BLACK)
    SetupAndPlayGame()



if __name__ == "__main__":
  global rows,cols
  rows=6
  cols=8
  global epsilon, myBrain

  BuildSeedFiles = False
  TrainFromModel = True

  numGamesToPlay = 2000
  with Pool(10) as pool:
        pool.map(GameRunBuildFiles,range(0,numGamesToPlay))



