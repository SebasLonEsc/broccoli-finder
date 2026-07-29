import random

from .broccoliProximity import broccoliProximity

# Calculates a valid random position for a broccoli
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   boardObject: the object containing all of the information about the board
# Output:
#   Returns an array of [row, column] position of a broccoli
def defineBroccoliPositions(board, boardObject):
  pos = [0,0]
  invalidPosition = True

  while invalidPosition:
    pos = [
      random.randrange(0, boardObject.totalRows),
      random.randrange(0, boardObject.totalColumns)
      ]
    if board[pos[0], pos[1]] >= 0:
      invalidPosition = False
  
  return pos

# Fills a board with a specific number of broccolis
# Input:
#   boardObject: the object containing all of the information about the board
#   broccoliAmount (optional): the number of broccolis on the board
#     default value is 1
# Output:
#   Returns the boardObject with the board matrix
#     filled with the specified amount of broccolis
def boardBroccoliFiller(boardObject, broccoliAmount = 1):
  board = boardObject.board
  totalRows = boardObject.totalRows
  totalColumns = boardObject.totalColumns

  if broccoliAmount >= boardObject.availableSpace:
    broccoliAmount = boardObject.availableSpace - 1

  for _ in range(broccoliAmount):
    pos = defineBroccoliPositions(board, boardObject)
    board[pos[0], pos[1]] = -1
    board = broccoliProximity(board, pos, totalRows, totalColumns)

  boardObject.changeBoard(board)
  boardObject.changeBroccoliAmount(broccoliAmount)

  return boardObject