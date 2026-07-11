import numpy as np
from .boardShaper import BoardShaper
from .broccoliFiller import BoardBroccoliFiller
from .constants.boardValues import BOARDTILEVALUE

def FillTilesBoard(tilesBoard):
  for i in range(0, tilesBoard.shape[0]):
    for j in range(0, tilesBoard.shape[1]):
      tilesBoard[i,j] = BOARDTILEVALUE.copy()

  return tilesBoard

class Board:
    def __init__(self, board, tilesBoard, rows, columns):
      self.board = board
      self.tilesBoard = tilesBoard
      self.totalRows = rows
      self.totalColumns = columns
      self.broccoliAmount = 0
      self.availableSpace = rows * columns
      self.nullSpaceNumber = 0
    
    def BoardSize(self):
      return self.totalRows * self.totalColumns
    
    def ChangeBoard(self, board):
      self.board = board

    def ChangeTilesBoard(self, tilesBoard):
      self.tilesBoard = tilesBoard

    def ChangeBroccoliAmount(self, broccoliAmount):
      self.broccoliAmount = broccoliAmount

    def ChangeAvaliableSpace(self, availableSpace):
      self.availableSpace = availableSpace

    def ChangeNullSpaceAmount(self, nullSpace):
      self.nullSpaceNumber = nullSpace

#Generates the Board Object
def BoardGenerator(rows, columns, broccoliAmount):
  emptyBoard = np.zeros(shape=[rows,columns],dtype=np.int8)
  tilesBoard = np.ndarray(shape=[rows,columns],dtype=np.object_)
  tilesBoard = FillTilesBoard(tilesBoard)
  
  boardObject = Board(
    emptyBoard,
    tilesBoard,
    rows,
    columns
  )

  boardObject = BoardShaper(boardObject)
  boardObject = BoardBroccoliFiller(boardObject, broccoliAmount)

  return boardObject