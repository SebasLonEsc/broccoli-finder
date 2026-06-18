import random
import numpy as np
from .constants.boardValues import *

def ShapeWeigher():
  boardShapesWeight = np.zeros(shape=[len(boardShapes)])
  boardShapesWeight[0] = 2

  for i in range(len(boardShapesWeight)):
    if i == 0:
      boardShapesWeight[0] = 2
      continue
    boardShapesWeight[i] = random.randint(1,2)

  return boardShapesWeight

#Return the board with the corners cut pattern
#Random values defines if the size of the cut is random or not
def cutCornersShaper(boardObject, random=False):
  return boardObject


#Return the board in a cross-shape pattern
def crossShaper(boardObject):
  #if(boardObject["totalRows"] == boardObject["totalColumns"] and boardObject["totalRows"] % 2 == 0):
  if(boardObject["totalRows"] == boardObject["totalColumns"] and boardObject["totalRows"] == 2):
    return boardObject
  
  if(boardObject["totalRows"] == 0 or boardObject["totalColumns"] == 2):
    return boardObject

  crossRow = random.randint(1, boardObject["totalRows"]-2)
  print(boardObject["totalRows"]-2)
  crossColumn = random.randint(1, boardObject["totalColumns"]-2)
  print(boardObject["totalColumns"]-2)
  board = boardObject["board"]

  for column in range(boardObject["totalColumns"]):
    board[crossRow, column] = -2

  for row in range(boardObject["totalRows"]):
    board[row, crossColumn] = -2

  boardObject["board"] = board

  return boardObject

#Returns a board in one of the shapes
def BoardShaper(boardObject):
  boardShapesWeight = ShapeWeigher()
  boardshape = "cross"#random.choices(boardShapes, boardShapesWeight)[0]
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