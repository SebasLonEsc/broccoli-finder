import numpy as np

from .boardShaper import boardShaper
from .broccoliFiller import boardBroccoliFiller
from .constants.boardValues import BOARDTILEVALUE

# Fills the each tile from the tiles board attribute with a dictionary.
#   And returns the filled matrix
# Input:
#   tilesBoard: matrix containing each tiles of the board
# Output:
#   tilesboard matrix fill with dictionaries for each tile on the board
def fillTilesBoard(tilesBoard):
  for i in range(0, tilesBoard.shape[0]):
    for j in range(0, tilesBoard.shape[1]):
      tilesBoard[i,j] = BOARDTILEVALUE.copy()

  return tilesBoard

# The board Class
#   board: the board matrix containg the information about:
#     nullspaces, broccoli position and proximity
#   tilesBoard: matrix containing each tiles of the board.
#     The tiles register the player progress.
#     And what the player sees in the interface or console
#   rows: the amount of rows of the board
#   columns: the amount of columns of the board
class Board:
    def __init__(self, board, tilesBoard, rows, columns):
      self.board = board
      self.tilesBoard = tilesBoard
      self.totalRows = rows
      self.totalColumns = columns
      self.broccoliAmount = 0
      self.availableSpace = rows * columns
      self.nullSpaceNumber = 0
    
    def boardSize(self):
      return self.totalRows * self.totalColumns
    
    def changeBoard(self, board):
      self.board = board

    def changeTilesBoard(self, tilesBoard):
      self.tilesBoard = tilesBoard

    def changeBroccoliAmount(self, broccoliAmount):
      self.broccoliAmount = broccoliAmount

    def changeAvaliableSpaces(self, availableSpace):
      self.availableSpace = availableSpace

    def changeNullSpacesAmount(self, nullSpace):
      self.nullSpaceNumber = nullSpace

    def flagTile(self, flaggedStatus, row, column):
      tile = self.tilesBoard[row, column]
      tile["flagged"] = flaggedStatus
      tilesBoard = self.tilesBoard
      tilesBoard[row, column] = tile

      self.changeTilesBoard(tilesBoard)

# Generates the Board Object, defines it shape and fills it with broccolis
# Input:
#   rows: the amount of rows of the board
#   columns: the amount of columns of the board
#   broccoliAmount: the amount of broccolis on the board
# Output:
#   Returns the generated board object
def boardGenerator(rows, columns, broccoliAmount):
  emptyBoard = np.zeros(shape=[rows, columns], dtype=np.int8)
  tilesBoard = np.ndarray(shape=[rows, columns], dtype=np.object_)
  tilesBoard = fillTilesBoard(tilesBoard)
  
  boardObject = Board(emptyBoard,
                      tilesBoard,
                      rows,
                      columns
                      )

  boardObject = boardShaper(boardObject)
  boardObject = boardBroccoliFiller(boardObject, broccoliAmount)

  return boardObject
