import numpy as np
import math
import random

from .constants.boardValues import BOARD_SHAPES, CORNER_GUIDE

def shapeWeigher(board_object):
  """Defines the weight of each avaiable board shape for the randomize.
 
  No-shaped board has a default weight of 2 for all iterations
  Args:
    board_object (Board): The object containing all of the information about the board
  Returns:
    np.ndarray: An array of the weights for each available baord shape
  """
  total_rows = board_object.total_rows
  total_columns = board_object.total_columns

  boardShapesWeight = np.zeros(shape=[len(BOARD_SHAPES)])
  boardShapesWeight[0] = 2
  i = 0

  for shape in BOARD_SHAPES:
    if i == 0: # Skiped normal board shape, default weight of 2
      i += 1
      continue

    if ((total_rows == 2 or total_columns == 2) and
        (shape == "cutCorners" or shape == "randomCutcorners")):
      boardShapesWeight[i] = 0
      i += 1
      continue

    if shape == "cross":
      if total_rows == 2 or total_columns == 2: # A two-lenght side will be reduce to one lenght on cross-shape
        boardShapesWeight[i] = 0
        i += 1
        continue

      board_size = total_rows * total_columns
      if board_size < 16:  # Cross-shaped Boards smaller than 16 size, had very little amount of playable tiles
        boardShapesWeight[i] = 0
        i += 1
        continue

    boardShapesWeight[i] = random.randint(1,2)
    i += 1

  return boardShapesWeight

def defineCornerSizes(board_object, randomCorners):
  """Define the corner size for cut corners shape (an random cut corners).

  In a normal cut corner shape all corner sizes are the same.
  For the random version shape, each corner has it own size.
  Which doesn't go beyond the half of the board horizontally or vertically
  Args:
    board_object (Board): The object containing all of the information about the board
    randomCorners (bool): Boolean indicating if each corner size is randomized
  Returns:
    np.ndarray: A matrix containg the sizes for each corner.
      In a [horizontalSize, verticalSize] pattern
  """
  cornerSizes = np.zeros((4,2), dtype=np.int_)
  total_rows = board_object.total_rows
  total_columns = board_object.total_columns
  horizontalCornerSizeLimit = math.floor(total_rows / 2)
  verticalCornerSizeLimit = math.floor(total_columns / 2)

  if total_rows % 2 == 0 and total_rows == 4:
    horizontalCornerSizeLimit -= 1

  if total_columns % 2 == 0 and total_columns == 4:
    verticalCornerSizeLimit -= 1

  if total_rows <= 2 or total_columns <= 2:
    return cornerSizes

  if randomCorners:
    for i in range(len(cornerSizes)):
      horizontalSize = random.randint(1, horizontalCornerSizeLimit)
      verticalSize = random.randint(1, verticalCornerSizeLimit)
      cornerSizes[i] = [horizontalSize, verticalSize]

  if not randomCorners:
    horizontalSize = random.randint(1, horizontalCornerSizeLimit)
    verticalSize = random.randint(1, verticalCornerSizeLimit)
    cornerSize = 1

    if(horizontalSize <= verticalSize):
      cornerSize = horizontalSize
    else:
      cornerSize = verticalSize

    for i in range(len(cornerSizes)):
      cornerSizes[i] = [cornerSize, cornerSize]
  
  return cornerSizes

def cutCornersShaper(board_object, randomCorners=False):
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
   randomCorners(bool): Indicates if each corner size is randomized (default False)
  Returns:
    Board: The board object with the updated information of the cutCorner shape
  """
  board = board_object.board
  tiles_board = board_object.tiles_board
  cornerSizes = defineCornerSizes(board_object, randomCorners)

  tile = {}
  null_space_amount = 0  

  for i in range(len(cornerSizes)):
    startPoint = 0
    endPoint = cornerSizes[i,0]

    if CORNER_GUIDE[i][0] == -1:
      startPoint = 0 - cornerSizes[i,0]
      endPoint = 0

    for j in range(startPoint, endPoint):
      tile = tiles_board[j, CORNER_GUIDE[i][1]]
      tile["tileValue"] = "*"
      tile["checked"] = True

      if board[j, CORNER_GUIDE[i][1]] == 0:
        board[j, CORNER_GUIDE[i][1]] = -2
        tiles_board[j, CORNER_GUIDE[i][1]] = tile
        null_space_amount += 1

    startPoint = 0
    endPoint = cornerSizes[i,1]

    if CORNER_GUIDE[i][1] == -1:
      startPoint = 0 - cornerSizes[i,1]
      endPoint = 0

    for j in range(startPoint, endPoint):
      tile = tiles_board[CORNER_GUIDE[i][0], j]
      tile["tileValue"] = "*"
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


def crossShaper(board_object):
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

  crossRow = random.randint(1, total_rows - 2)
  crossColumn = random.randint(1, total_columns - 2)
  board = board_object.board
  tiles_board = board_object.tiles_board

  tile = {}
  null_space_amount = 0

  for column in range(total_columns):
    tile = tiles_board[crossRow, column]
    tile["tileValue"] = "*"
    tile["checked"] = True
    
    board[crossRow, column] = -2
    tiles_board[crossRow, column] = tile
    null_space_amount += 1

  for row in range(total_rows):
    if board[row, crossColumn] == -2:
      continue

    tile = tiles_board[row, crossColumn]
    tile["tileValue"] = "*"
    tile["checked"] = True

    board[row, crossColumn] = -2
    tiles_board[row, crossColumn] = tile
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
  boardShapesWeight = shapeWeigher(board_object)
  boardShape = random.choices(BOARD_SHAPES, boardShapesWeight)[0]
  shapedBoard = board_object

  match boardShape:
    case "cutCorners":
      shapedBoard = cutCornersShaper(shapedBoard)
    case "cross":
      shapedBoard = crossShaper(shapedBoard)
    case "randomCutcorners":
      shapedBoard = cutCornersShaper(shapedBoard, True)

  return shapedBoard