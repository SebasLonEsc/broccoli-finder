import numpy as np

from .boardShaper import board_shaper
from .broccoliFiller import board_broccoli_filler
from .constants.boardValues import BOARD_TILE_VALUE

def fill_tiles_board(tiles_board):
  """Fills each tile from the tiles_board attribute with a dictionary.
  
  Args:
    tiles_board (np.ndarray): Matrix containing each tiles of the board
  Returns:
    np.ndarray: Filled tiles_board matrix with dictionaries, one for each tile on the board
  """
  for i in range(0, tiles_board.shape[0]):
    for j in range(0, tiles_board.shape[1]):
      tiles_board[i,j] = BOARD_TILE_VALUE.copy()

  return tiles_board

class Board:
  """The board Class.

  Args:
    board (np.dnarray): The board matrix containg the information about:
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board.
      The tiles register the player progress.
      And what the player sees in the interface or console
    rows (int): The amount of rows of the board
    columns (int): The amount of columns of the board
  """
  def __init__(self, board, tiles_board, rows, columns):
    self.board = board
    self.tiles_board = tiles_board
    self.total_rows = rows
    self.total_columns = columns
    self.broccoli_amount = 0
    self.available_space = rows * columns
    self.null_space_amount = 0
  
  def board_size(self):
    return self.total_rows * self.total_columns
  
  def change_board(self, board):
    self.board = board

  def change_tiles_board(self, tiles_board):
    self.tiles_board = tiles_board

  def change_broccoli_amount(self, broccoli_amount):
    self.broccoli_amount = broccoli_amount

  def change_avaliable_spaces_amount(self, available_space):
    self.available_space = available_space

  def change_null_spaces_amount(self, null_spaces_amount):
    self.null_space_amount = null_spaces_amount

  def flag_tile(self, flagged_status, row, column):
    tile = self.tiles_board[row, column]
    tile["flagged"] = flagged_status
    tiles_board = self.tiles_board
    tiles_board[row, column] = tile

    self.change_tiles_board(tiles_board)

def board_generator(rows, columns, broccoli_amount):
  """Generates the Board Object, defines it shape and fills it with broccolis.

  Args:
    rows (int): The amount of rows of the board
    columns (int): The amount of columns of the board
    broccoli_amount (int): The amount of broccolis on the board
  Returns:
    Board: The board object
  """
  empty_board = np.zeros(shape=[rows, columns], dtype=np.int8)
  tiles_board = np.ndarray(shape=[rows, columns], dtype=np.object_)
  tiles_board = fill_tiles_board(tiles_board)
  
  board_object = Board(empty_board,
                       tiles_board,
                       rows,
                       columns
                       )

  board_object = board_shaper(board_object)
  board_object = board_broccoli_filler(board_object, broccoli_amount)

  return board_object
