import numpy as np
from .boardShaper import BoardShaper
from .broccoliFiller import BoardBroccoliFiller

def BoardGenerator(rows, columns, broccoliAmount):
  emptyBoard = np.zeros(shape=[rows,columns],dtype=np.int8)
  
  boardObject = {
    "board": emptyBoard,
    "totalRows": rows,
    "totalColumns": columns,
    "boardSize": rows * columns,
    "broccoliAmount": 0,
    "availableSpace": rows * columns,
    "nullSpaceNumber": 0
  }

  shapedBoardObject = BoardShaper(boardObject)
  shapedBoardObject = BoardBroccoliFiller(shapedBoardObject, broccoliAmount)

  return shapedBoardObject