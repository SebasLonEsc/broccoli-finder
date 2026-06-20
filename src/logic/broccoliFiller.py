import random
from .broccoliProximity import broccoliProximity

#Calculates a valid random position for a broccoli
def DefineBroccoliPositions(board, boardObject):
  pos = [0,0]
  invalidPosition = True

  while invalidPosition:
    pos = [random.randrange(0, boardObject["totalRows"]), random.randrange(0, boardObject["totalColumns"])]
    if board[pos[0], pos[1]] >= 0:
      invalidPosition = False
  
  return pos

#Fills a board with an specific number of broccolis
def BoardBroccoliFiller(boardObject, broccoliAmount = 1):
  board = boardObject["board"]
  totalRows = boardObject["totalRows"]
  totalColumns = boardObject["totalColumns"]

  if broccoliAmount >= boardObject["availableSpace"]:
    broccoliAmount = boardObject["availableSpace"] - 1

  for i in range(broccoliAmount):
    pos = DefineBroccoliPositions(board, boardObject)
    board[pos[0], pos[1]] = -1
    board = broccoliProximity(board, pos, totalRows, totalColumns)

  boardObject["board"] = board
  boardObject["broccoliAmount"] = broccoliAmount

  return boardObject