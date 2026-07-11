import random
import numpy as np
import math
from .constants.boardValues import BOARDSHAPES, CORNERGUIDE

def ShapeWeigher(boardObject):
  boardShapesWeight = np.zeros(shape=[len(BOARDSHAPES)])
  boardShapesWeight[0] = 2
  i = 0

  for shape in BOARDSHAPES:
    if i == 0:
      i += 1
      continue

    if (boardObject.totalRows == 2 or boardObject.totalColumns == 2) and (shape == "cutCorners" or shape == "randomCutcorners"):
      boardShapesWeight[i] = 2
      i += 1
      continue

    boardShapesWeight[i] = random.randint(1,2)
    i += 1

  return boardShapesWeight

def defineCornerSizes(boardObject, randomCorners):
  cornerSizes = np.zeros((4,2), dtype=np.int_)
  horizontalCornerSizeLimit = math.floor(boardObject.totalRows / 2)
  verticalCornerSizeLimit = math.floor(boardObject.totalColumns / 2)

  if boardObject.totalRows % 2 == 0:
    horizontalCornerSizeLimit -= 1

  if boardObject.totalColumns % 2 == 0:
    verticalCornerSizeLimit -= 1

  if boardObject.totalRows <= 2 or boardObject.totalColumns <= 2:
    return cornerSizes

  if randomCorners:
    for i in range(len(cornerSizes)):
      horizontalSize = random.randint(1,horizontalCornerSizeLimit)
      verticalSize = random.randint(1,verticalCornerSizeLimit)
      cornerSizes[i] = [horizontalSize, verticalSize]

  if not randomCorners:
    horizontalSize = random.randint(1,horizontalCornerSizeLimit)
    verticalSize = random.randint(1,verticalCornerSizeLimit)
    cornerSize = 1

    if(horizontalSize <= verticalSize):
      cornerSize = horizontalSize
    else:
      cornerSize = verticalSize

    for i in range(len(cornerSizes)):
      cornerSizes[i] = [cornerSize, cornerSize]
  
  return cornerSizes

#Return the board with the corners cut pattern
#Random values defines if the size of the cut is random or not
#Position of each corner size c:corner #:Corner position
# c0 0 c1
#  0 0 0
# c2 0 c3
#Each position is an array of two values [r,c]
#r:row or horizontal
#c:column or vertical
def CutCornersShaper(boardObject, randomCorners=False):
  board = boardObject.board
  tilesBoard = boardObject.tilesBoard
  cornerSizes = defineCornerSizes(boardObject, randomCorners)

  tile = {}
  nullSpaceNumber = 0  

  for i in range(len(cornerSizes)):
    startPoint = 0
    endPoint = cornerSizes[i,0]

    if CORNERGUIDE[i][0] == -1:
      startPoint = 0 - cornerSizes[i,0]
      endPoint = 0

    for j in range(startPoint, endPoint):
      tile = tilesBoard[j, CORNERGUIDE[i][1]]
      tile["tileValue"] = "*"
      tile["checked"] = True

      board[j, CORNERGUIDE[i][1]] = -2
      tilesBoard[j, CORNERGUIDE[i][1]] = tile
      nullSpaceNumber += 1

    startPoint = 0
    endPoint = cornerSizes[i,1]

    if CORNERGUIDE[i][1] == -1:
      startPoint = 0 - cornerSizes[i,1]
      endPoint = 0

    for j in range(startPoint, endPoint):
      tile = tilesBoard[CORNERGUIDE[i][0], j]
      tile["tileValue"] = "*"
      tile["checked"] = True

      board[CORNERGUIDE[i][0], j] = -2
      tilesBoard[CORNERGUIDE[i][0], j] = tile
      nullSpaceNumber += 1
    
  boardObject.ChangeBoard(board)
  boardObject.ChangeTilesBoard(tilesBoard)
  boardObject.ChangeNullSpaceAmount(nullSpaceNumber)
  boardObject.ChangeAvaliableSpace(boardObject.BoardSize() - nullSpaceNumber)

  return boardObject


#Return the board in a cross-shape pattern
def CrossShaper(boardObject):
  if(boardObject.totalRows == boardObject.totalColumns and boardObject.totalRows == 2):
    return boardObject
  
  if(boardObject.totalRows == 2 or boardObject.totalColumns == 2):
    return boardObject

  crossRow = random.randint(1, boardObject.totalRows-2)
  crossColumn = random.randint(1, boardObject.totalColumns-2)
  board = boardObject.board
  tilesBoard = boardObject.tilesBoard

  tile = {}
  nullSpaceNumber = 0

  for column in range(boardObject.totalColumns):
    tile = tilesBoard[crossRow, column]
    tile["tileValue"] = "*"
    tile["checked"] = True
    
    board[crossRow, column] = -2
    tilesBoard[crossRow, column] = tile
    nullSpaceNumber += 1

  for row in range(boardObject.totalRows):
    if board[row, crossColumn] == -2:
      continue

    tile = tilesBoard[row, crossColumn]
    tile["tileValue"] = "*"
    tile["checked"] = True

    board[row, crossColumn] = -2
    tilesBoard[row, crossColumn] = tile
    nullSpaceNumber += 1

  boardObject.ChangeBoard(board)
  boardObject.ChangeTilesBoard(tilesBoard)
  boardObject.ChangeNullSpaceAmount(nullSpaceNumber)
  boardObject.ChangeAvaliableSpace(boardObject.BoardSize() - nullSpaceNumber)

  return boardObject

#Returns a board in one of the shapes
def BoardShaper(boardObject):
  boardShapesWeight = ShapeWeigher(boardObject)
  boardshape = random.choices(BOARDSHAPES, boardShapesWeight)[0]
  shapedBoard = boardObject

  match boardshape:
    case "cutCorners":
      shapedBoard = CutCornersShaper(shapedBoard)
    case "cross":
      shapedBoard = CrossShaper(shapedBoard)
    case "randomCutcorners":
      shapedBoard = CutCornersShaper(shapedBoard, True)

  return shapedBoard