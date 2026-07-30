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
      random.randrange(0, boardObject.total_rows),
      random.randrange(0, boardObject.total_columns)
      ]
    if board[pos[0], pos[1]] >= 0:
      invalidPosition = False
  
  return pos

def board_broccoli_filler(boardObject, broccoli_amount=1):
  """Fills a board with a specific number of broccolis.

  Args:
    boardObject (Board): The object containing all of the information about the board
    broccoli_amount (int): The number of broccolis on the board (default 1)
  Returns:
    Board: The boardObject with the board matrix filled the specified amount of broccolis
  """
  board = boardObject.board
  total_rows = boardObject.total_rows
  total_columns = boardObject.total_columns

  if broccoli_amount >= boardObject.available_space:
    broccoli_amount = boardObject.available_space - 1

  for _ in range(broccoli_amount):
    pos = defineBroccoliPositions(board, boardObject)
    board[pos[0], pos[1]] = -1
    board = broccoliProximity(board, pos, total_rows, total_columns)

  boardObject.change_board(board)
  boardObject.change_broccoli_amount(broccoli_amount)

  return boardObject