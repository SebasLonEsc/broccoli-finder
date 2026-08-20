import numpy as np
import math
import random

from .constants.boardValues import BOARD_SHAPES, CORNER_GUIDE

def shapes_weight_definer(board_object):
  """Defines the weight of each avaiable board shape for the randomize.
 
  No-shaped board has a default weight of 2 for all iterations
  Args:
    board_object (Board): The object containing all of the information about the board
  Returns:
    np.ndarray: An array of the weights for each available baord shape
  """
  total_rows = board_object.total_rows
  total_columns = board_object.total_columns

  board_shapes_weight = np.zeros(shape=[len(BOARD_SHAPES)])
  board_shapes_weight[0] = 2
  i = 0

  for shape in BOARD_SHAPES:
    if i == 0: # Skiped normal board shape, default weight of 2
      i += 1
      continue

    if ((total_rows == 2 or total_columns == 2) and
        (shape == "cutCorners" or shape == "randomCutcorners")):
      board_shapes_weight[i] = 0
      i += 1
      continue

    if shape == "cross":
      if total_rows == 2 or total_columns == 2: # A two-lenght side will be reduce to one lenght on cross-shape
        board_shapes_weight[i] = 0
        i += 1
        continue

      board_size = total_rows * total_columns
      if board_size < 16:  # Cross-shaped Boards smaller than 16 size, had very little amount of playable tiles
        board_shapes_weight[i] = 0
        i += 1
        continue

    board_shapes_weight[i] = random.randint(1,2)
    i += 1

  return board_shapes_weight

def define_corner_sizes(board_object, random_corners):
  """Define the corner size for cut corners shape (an random cut corners).

  In a normal cut corner shape all corner sizes are the same.
  For the random version shape, each corner has it own size.
  Which doesn't go beyond the half of the board horizontally or vertically
  Args:
    board_object (Board): The object containing all of the information about the board
    random_corners (bool): Boolean indicating if each corner size is randomized
  Returns:
    np.ndarray: A matrix containg the sizes for each corner.
      In a [horizontal_size, vertical_size] pattern
  """
  corner_sizes = np.zeros((4,2), dtype=np.int_)
  total_rows = board_object.total_rows
  total_columns = board_object.total_columns
  horizontal_corner_size_limit = math.floor(total_rows / 2)
  vertical_corner_size_limit = math.floor(total_columns / 2)

  if total_rows % 2 == 0 and total_rows == 4:
    horizontal_corner_size_limit -= 1

  if total_columns % 2 == 0 and total_columns == 4:
    vertical_corner_size_limit -= 1

  if total_rows <= 2 or total_columns <= 2:
    return corner_sizes

  if random_corners:
    for i in range(len(corner_sizes)):
      horizontal_size = random.randint(1, horizontal_corner_size_limit)
      vertical_size = random.randint(1, vertical_corner_size_limit)
      corner_sizes[i] = [horizontal_size, vertical_size]

  if not random_corners:
    horizontal_size = random.randint(1, horizontal_corner_size_limit)
    vertical_size = random.randint(1, vertical_corner_size_limit)
    corner_size = 1

    if(horizontal_size <= vertical_size):
      corner_size = horizontal_size
    else:
      corner_size = vertical_size

    for i in range(len(corner_sizes)):
      corner_sizes[i] = [corner_size, corner_size]
  
  return corner_sizes

def cut_corners_shaper(board_object, random_corners=False):
  """Shapes the board in a with its corners cut.

  Random values defines if the size of the cut is random or not.
  Position of each corner size is c# where c:corner #:Corner position

  c0 0 c1
  
  0 0 0
  
  c2 0 c3

  Each position is an array of two values [r,c]
  r:row or horizontal
  c:column or vertical
  Args:
   board_object (Board): The object containing all of the information about the board
   random_corners(bool): Indicates if each corner size is randomized (default False)
  Returns:
    Board: The board object with the updated information of the cutCorner shape
  """
  board = board_object.board
  tiles_board = board_object.tiles_board
  corner_sizes = define_corner_sizes(board_object, random_corners)

  tile = {}
  null_space_amount = 0  

  for i in range(len(corner_sizes)):
    start_point = 0
    end_point = corner_sizes[i,0]

    if CORNER_GUIDE[i][0] == -1:
      start_point = 0 - corner_sizes[i,0]
      end_point = 0

    for j in range(start_point, end_point):
      tile = tiles_board[j, CORNER_GUIDE[i][1]]
      tile["tileValue"] = -2
      tile["checked"] = True

      if board[j, CORNER_GUIDE[i][1]] == 0:
        board[j, CORNER_GUIDE[i][1]] = -2
        tiles_board[j, CORNER_GUIDE[i][1]] = tile
        null_space_amount += 1

    start_point = 0
    end_point = corner_sizes[i,1]

    if CORNER_GUIDE[i][1] == -1:
      start_point = 0 - corner_sizes[i,1]
      end_point = 0

    for j in range(start_point, end_point):
      tile = tiles_board[CORNER_GUIDE[i][0], j]
      tile["tileValue"] = -2
      tile["checked"] = True

      if board[CORNER_GUIDE[i][0], j] == 0:
        board[CORNER_GUIDE[i][0], j] = -2
        tiles_board[CORNER_GUIDE[i][0], j] = tile
        null_space_amount += 1
    
  board_object.change_board(board)
  board_object.change_tiles_board(tiles_board)
  board_object.change_null_spaces_amount(null_space_amount)
  board_object.change_avaliable_spaces_amount(board_object.board_size() - null_space_amount)

  return board_object


def cross_shaper(board_object):
  """Shapes the board in a cross-like shape.

  The row and column of the cross are selected randomly.
  Without including the first and last row/column
  Args:
    board_object (Board): The object containing all of the information about the board
  Returns:
    Board: The board object with the updated information of the cross shape
  """
  total_rows = board_object.total_rows
  total_columns = board_object.total_columns

  if(total_rows <= 3 or total_columns <= 3):
    # For side of length 3 the available space it's too little
    return board_object
  
  if(total_rows * total_columns <= 16):
    # Blocks 4x4 boards on having cross shape
    return board_object

  cross_row = random.randint(1, total_rows - 2)
  cross_column = random.randint(1, total_columns - 2)
  board = board_object.board
  tiles_board = board_object.tiles_board

  tile = {}
  null_space_amount = 0

  for column in range(total_columns):
    tile = tiles_board[cross_row, column]
    tile["tileValue"] = -2
    tile["checked"] = True
    
    board[cross_row, column] = -2
    tiles_board[cross_row, column] = tile
    null_space_amount += 1

  for row in range(total_rows):
    if board[row, cross_column] == -2:
      continue

    tile = tiles_board[row, cross_column]
    tile["tileValue"] = -2
    tile["checked"] = True

    board[row, cross_column] = -2
    tiles_board[row, cross_column] = tile
    null_space_amount += 1

  board_object.change_board(board)
  board_object.change_tiles_board(tiles_board)
  board_object.change_null_spaces_amount(null_space_amount)
  board_object.change_avaliable_spaces_amount(board_object.board_size() - null_space_amount)

  return board_object

def board_shaper(board_object):
  """Handles the shaping of the board.

  Args:
    board_object (Board): The object containing all of the information about the board
  Returns:
    Board: The board object in a randomly selected shape
  """
  board_shapes_weight = shapes_weight_definer(board_object)
  board_shape = random.choices(BOARD_SHAPES, board_shapes_weight)[0]
  shaped_board = board_object

  match board_shape:
    case "cutCorners":
      shaped_board = cut_corners_shaper(shaped_board)
    case "cross":
      shaped_board = cross_shaper(shaped_board)
    case "randomCutcorners":
      shaped_board = cut_corners_shaper(shaped_board, True)

  return shaped_board