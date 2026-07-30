import random

from .broccoliProximity import broccoliProximity

def defineBroccoliPositions(board, boardObject):
  """Calculates a valid random position for a broccoli.

  Args:
    board (np.ndarray): The board matrix containg the information about:
      nullspaces, broccoli position and proximity
    boardObject (Board): The object containing all of the information about the board
  Returns:
    array[int]: An array of [row, column] position of a broccoli
  """
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

def boardBroccoliFiller(boardObject, broccoliAmount=1):
  """Fills a board with a specific number of broccolis.

  Args:
    boardObject (Board): The object containing all of the information about the board
    broccoliAmount (int): The number of broccolis on the board (default 1)
  Returns:
    Board: The boardObject with the board matrix filled the specified amount of broccolis
  """
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