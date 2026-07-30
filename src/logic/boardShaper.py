import numpy as np
import math
import random

from .constants.boardValues import BOARDSHAPES, CORNERGUIDE

def shapeWeigher(boardObject):
  """Defines the weight of each avaiable board shape for the randomize.
 
  No-shaped board has a default weight of 2 for all iterations
  Args:
    boardObject (Board): The object containing all of the information about the board
  Returns:
    np.ndarray: An array of the weights for each available baord shape
  """
  total_rows = boardObject.total_rows
  total_columns = boardObject.total_columns

  boardShapesWeight = np.zeros(shape=[len(BOARDSHAPES)])
  boardShapesWeight[0] = 2
  i = 0

  for shape in BOARDSHAPES:
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

def defineCornerSizes(boardObject, randomCorners):
  """Define the corner size for cut corners shape (an random cut corners).

  In a normal cut corner shape all corner sizes are the same.
  For the random version shape, each corner has it own size.
  Which doesn't go beyond the half of the board horizontally or vertically
  Args:
    boardObject (Board): The object containing all of the information about the board
    randomCorners (bool): Boolean indicating if each corner size is randomized
  Returns:
    np.ndarray: A matrix containg the sizes for each corner.
      In a [horizontalSize, verticalSize] pattern
  """
  cornerSizes = np.zeros((4,2), dtype=np.int_)
  total_rows = boardObject.total_rows
  total_columns = boardObject.total_columns
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

def cutCornersShaper(boardObject, randomCorners=False):
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
   boardObject (Board): The object containing all of the information about the board
   randomCorners(bool): Indicates if each corner size is randomized (default False)
  Returns:
    Board: The board object with the updated information of the cutCorner shape
  """
  board = boardObject.board
  tiles_board = boardObject.tiles_board
  cornerSizes = defineCornerSizes(boardObject, randomCorners)

  tile = {}
  null_space_amount = 0  

  for i in range(len(cornerSizes)):
    startPoint = 0
    endPoint = cornerSizes[i,0]

    if CORNERGUIDE[i][0] == -1:
      startPoint = 0 - cornerSizes[i,0]
      endPoint = 0

    for j in range(startPoint, endPoint):
      tile = tiles_board[j, CORNERGUIDE[i][1]]
      tile["tileValue"] = "*"
      tile["checked"] = True

      if board[j, CORNERGUIDE[i][1]] == 0:
        board[j, CORNERGUIDE[i][1]] = -2
        tiles_board[j, CORNERGUIDE[i][1]] = tile
        null_space_amount += 1

    startPoint = 0
    endPoint = cornerSizes[i,1]

    if CORNERGUIDE[i][1] == -1:
      startPoint = 0 - cornerSizes[i,1]
      endPoint = 0

    for j in range(startPoint, endPoint):
      tile = tiles_board[CORNERGUIDE[i][0], j]
      tile["tileValue"] = "*"
      tile["checked"] = True

      if board[CORNERGUIDE[i][0], j] == 0:
        board[CORNERGUIDE[i][0], j] = -2
        tiles_board[CORNERGUIDE[i][0], j] = tile
        null_space_amount += 1
    
  boardObject.change_board(board)
  boardObject.change_tiles_board(tiles_board)
  boardObject.change_null_spaces_amount(null_space_amount)
  boardObject.change_avaliable_spaces_amount(boardObject.board_size() - null_space_amount)

  return boardObject


def crossShaper(boardObject):
  """Shapes the board in a cross-like shape.

  The row and column of the cross are selected randomly.
  Without including the first and last row/column
  Args:
     boardObject (Board): The object containing all of the information about the board
    Returns:
      Board: The board object with the updated information of the cross shape
  """
  total_rows = boardObject.total_rows
  total_columns = boardObject.total_columns

  if(total_rows <= 3 or total_columns <= 3):
    # For side of length 3 the available space it's too little
    return boardObject
  
  if(total_rows * total_columns <= 16):
    # Blocks 4x4 boards on having cross shape
    return boardObject

  crossRow = random.randint(1, total_rows - 2)
  crossColumn = random.randint(1, total_columns - 2)
  board = boardObject.board
  tiles_board = boardObject.tiles_board

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

  boardObject.change_board(board)
  boardObject.change_tiles_board(tiles_board)
  boardObject.change_null_spaces_amount(null_space_amount)
  boardObject.change_avaliable_spaces_amount(boardObject.board_size() - null_space_amount)

  return boardObject

def board_shaper(boardObject):
  """Handles the shaping of the board.

  Args:
    boardObject (Board): The object containing all of the information about the board
  Returns:
    Board: The board object in a randomly selected shape
  """
  boardShapesWeight = shapeWeigher(boardObject)
  boardShape = random.choices(BOARDSHAPES, boardShapesWeight)[0]
  shapedBoard = boardObject

  match boardShape:
    case "cutCorners":
      shapedBoard = cutCornersShaper(shapedBoard)
    case "cross":
      shapedBoard = crossShaper(shapedBoard)
    case "randomCutcorners":
      shapedBoard = cutCornersShaper(shapedBoard, True)

  return shapedBoard