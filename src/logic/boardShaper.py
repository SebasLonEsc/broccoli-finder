import random
import numpy as np
import math
from .constants.boardValues import boardShapes, cornerGuide

def ShapeWeigher(boardObject):
  boardShapesWeight = np.zeros(shape=[len(boardShapes)])
  boardShapesWeight[0] = 2
  i = 0

  for shape in boardShapes:
    if i == 0:
      i += 1
      continue

    if (boardObject["totalRows"] == 2 or boardObject["totalRows"] == 2) and (shape == "cutCorners" or shape == "randomCutcorners"):
      boardShapesWeight[i] = 2
      i += 1
      continue

    boardShapesWeight[i] = random.randint(1,2)
    i += 1

  return boardShapesWeight

def defineCornerSizes(boardObject, randomCorners):
  cornerSizes = np.zeros((4,2), dtype=np.int_)
  horizontalCornerSizeLimit = math.floor(boardObject["totalRows"] / 2)
  verticalCornerSizeLimit = math.floor(boardObject["totalColumns"] / 2)

  if boardObject["totalRows"] % 2 == 0:
    horizontalCornerSizeLimit -= 1

  if boardObject["totalColumns"] % 2 == 0:
    verticalCornerSizeLimit -= 1

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
def cutCornersShaper(boardObject, randomCorners=False):
  board = boardObject["board"]
  cornerSizes = defineCornerSizes(boardObject, randomCorners)

  for i in range(len(cornerSizes)):
    startPoint = 0
    endPoint = cornerSizes[i,0]

    if cornerGuide[i][0] == -1:
      startPoint = 0 - cornerSizes[i,0]
      endPoint = 0

    for j in range(startPoint, endPoint):
      board[j, cornerGuide[i][1]] = -2

    startPoint = 0
    endPoint = cornerSizes[i,1]

    if cornerGuide[i][1] == -1:
      startPoint = 0 - cornerSizes[i,1]
      endPoint = 0

    for j in range(startPoint, endPoint):
      board[cornerGuide[i][0], j] = -2
    
  boardObject["board"] = board

  return boardObject


#Return the board in a cross-shape pattern
def crossShaper(boardObject):
  if(boardObject["totalRows"] == boardObject["totalColumns"] and boardObject["totalRows"] == 2):
    return boardObject
  
  if(boardObject["totalRows"] == 2 or boardObject["totalColumns"] == 2):
    return boardObject

  crossRow = random.randint(1, boardObject["totalRows"]-2)
  crossColumn = random.randint(1, boardObject["totalColumns"]-2)
  board = boardObject["board"]
  nullSpaceNumber = 0

  for column in range(boardObject["totalColumns"]):
    board[crossRow, column] = -2
    nullSpaceNumber += 1

  for row in range(boardObject["totalRows"]):
    if board[row, crossColumn] == -2:
      continue

    board[row, crossColumn] = -2
    nullSpaceNumber += 1

  boardObject["board"] = board
  boardObject["nullSpaceNumber"] = nullSpaceNumber
  boardObject["availableSpace"] = boardObject["boardSize"] - nullSpaceNumber

  return boardObject

#Returns a board in one of the shapes
def BoardShaper(boardObject):
  boardShapesWeight = ShapeWeigher(boardObject)
  boardshape = "cutCorners"#random.choices(boardShapes, boardShapesWeight)[0]
  print(boardshape)
  shapedBoard = boardObject

  match boardshape:
    case "cutCorners":
      shapedBoard = cutCornersShaper(shapedBoard)
    case "cross":
      shapedBoard = crossShaper(shapedBoard)
    case "randomCutcorners":
      shapedBoard = cutCornersShaper(shapedBoard, True)

  return shapedBoard