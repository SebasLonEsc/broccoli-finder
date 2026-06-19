import numpy as np
from .boardShaper import BoardShaper
from .broccoliFiller import BoardBroccoliFiller

#Generates the Board Object
def BoardGenerator(rows, columns, broccoliAmount):
  emptyBoard = np.zeros(shape=[rows,columns],dtype=np.int8)
  
  boardObject = {
    "board": emptyBoard,
    "viewedBoard": emptyBoard,
    "totalRows": rows,
    "totalColumns": columns,
    "boardSize": rows * columns,
    "broccoliAmount": 0,
    "availableSpace": rows * columns,
    "nullSpaceNumber": 0
  }

  boardObject = BoardShaper(boardObject)
  boardObject = BoardBroccoliFiller(boardObject, broccoliAmount)

  return boardObject