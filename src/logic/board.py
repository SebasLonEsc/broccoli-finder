import numpy as np

from .boardShaper import boardShaper
from .broccoliFiller import boardBroccoliFiller
from .constants.boardValues import BOARDTILEVALUE

def fillTilesBoard(tilesBoard):
  """Fills each tile from the tilesBoard attribute with a dictionary.
  
  Args:
    tilesBoard (np.ndarray): Matrix containing each tiles of the board
  Output:
    np.ndarray: Filled tilesboard matrix with dictionaries, one for each tile on the board
  """
  for i in range(0, tilesBoard.shape[0]):
    for j in range(0, tilesBoard.shape[1]):
      tilesBoard[i,j] = BOARDTILEVALUE.copy()

  return tilesBoard

class Board:
  """The board Class.

  Args:
    board (np.dnarray): The board matrix containg the information about:
      nullspaces, broccoli position and proximity
    tilesBoard (np.ndarray): Matrix containing each tiles of the board.
      The tiles register the player progress.
      And what the player sees in the interface or console
    rows (int): The amount of rows of the board
    columns (int): The amount of columns of the board
  """
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

def board_generator(rows, columns, broccoliAmount):
  """Generates the Board Object, defines it shape and fills it with broccolis.

  Args:
    rows (int): The amount of rows of the board
    columns (int): The amount of columns of the board
    broccoliAmount (int): The amount of broccolis on the board
  Returns:
    Board: The board object
  """
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
