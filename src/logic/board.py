import numpy as np
from .boardShaper import BoardShaper
from .broccoliFiller import BoardBroccoliFiller
from .constants.boardValues import boardTileValue

def FillTilesBoard(tilesBoard):
  for i in range(0, tilesBoard.shape[0]):
    for j in range(0, tilesBoard.shape[1]):
      tilesBoard[i,j] = boardTileValue.copy()

  return tilesBoard

#Generates the Board Object
def BoardGenerator(rows, columns, broccoliAmount):
  emptyBoard = np.zeros(shape=[rows,columns],dtype=np.int8)
  tilesBoard = np.ndarray(shape=[rows,columns],dtype=np.object_)
  tilesBoard = FillTilesBoard(tilesBoard)
  
  boardObject = {
    "board": emptyBoard,
    "tilesBoard": tilesBoard,
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