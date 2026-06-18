import numpy as np
from .boardShaper import BoardShaper

#Fills a board with an specific number of broccolis
def BoardBroccoliFiller(board, broccolisAmount):
  return 0

def BoardGenerator(rows, columns):
  emptyBoard = np.zeros(shape=[rows,columns],dtype=np.int8)
  
  boardObject = {
    "board": emptyBoard,
    "totalRows": rows,
    "totalColumns": columns,
    "boardSize": rows * columns,
    "numberBroccolis": 0,
    "availableSpace": rows * columns,
  }
  shapedBoardObject = BoardShaper(boardObject)

  return shapedBoardObject