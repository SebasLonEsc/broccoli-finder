import numpy as np

from .boardShaper import board_shaper
from .boardFiller import board_broccoli_filler
from .constants.boardValues import BOARD_TILE_VALUE

def fill_tiles_board(tiles_board):
  """Fills each tile from the tiles_board attribute with a dictionary.
  
  Args:
    tiles_board (np.ndarray): Matrix containing each tiles of the board.
      The tiles register the player progress.
      And what the player sees in the interface or console
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
    rows (int): The amount of rows of the board
    columns (int): The amount of columns of the board
  """
  def __init__(self, rows, columns):
    empty_tiles_board = np.ndarray(shape=[rows, columns], dtype=np.object_)

    self.board = np.zeros(shape=[rows, columns], dtype=np.int8)
    self.tiles_board = fill_tiles_board(empty_tiles_board)
    self.total_rows = rows
    self.total_columns = columns
    self.broccoli_amount = 0
    self.available_space = rows * columns
    self.null_space_amount = 0
    self.broccoli_positions = []
  
  def board_size(self):
    return self.total_rows * self.total_columns
  
  def change_board(self, board):
    """Changes the board array attribute

    Args:
      board (np.dnarray): The board matrix containg the information about:
      nullspaces, broccoli position and proximity
    """
    self.board = board

  def change_tiles_board(self, tiles_board):
    """Changes the tiles_board attribute

    Args:
      tiles_board (np.ndarray): Matrix containing each tiles of the board.
        The tiles register the player progress.
        And what the player sees in the interface or console
    """
    self.tiles_board = tiles_board

  def change_broccoli_amount(self, broccoli_amount):
    """Changes the broccoli amount attribute

    Args:
      broccoli_amount (int): The total broccoli amount on the board
    """
    self.broccoli_amount = broccoli_amount

  def change_avaliable_spaces_amount(self, available_space):
    """Changes the avaiable space amount attribute

    Args:
      avaiable_space (int): The total available space on the board
    """
    self.available_space = available_space

  def change_null_spaces_amount(self, null_spaces_amount):
    """Changes the nullspaces amount attribute

    Args:
      null_spaces_amount (int): The total nullspace amount on the board
    """
    self.null_space_amount = null_spaces_amount

  def flag_tile(self, flagged_status, row, column):
    """Flags a specific tile on the board

    Args:
      flagged_status (bool): The new flagged status of the tile
      row (int): The row position of the tile
      column (int): The column position of the tile
    """
    tile = self.tiles_board[row, column]
    tile["flagged"] = flagged_status
    tiles_board = self.tiles_board
    tiles_board[row, column] = tile

    self.change_tiles_board(tiles_board)

  def add_broccoli_positions(self, position):
    """Registers a broccoli position

    Args:
      position (array[int. int]): The position of the added broccoli
    """
    self.broccoli_positions.append(position)

def board_generator(rows, columns, broccoli_amount):
  """Generates the Board Object, defines it shape and fills it with broccolis.

  Args:
    rows (int): The amount of rows of the board
    columns (int): The amount of columns of the board
    broccoli_amount (int): The amount of broccolis on the board
  Returns:
    Board: The board object
  """  
  board_object = Board(rows,
                       columns
                       )

  board_object = board_shaper(board_object)
  board_object = board_broccoli_filler(board_object, broccoli_amount)

  return board_object
