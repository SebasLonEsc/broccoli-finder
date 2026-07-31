import random

from .broccoliProximity import broccoliProximity

def defineBroccoliPositions(board, board_object):
  """Calculates a valid random position for a broccoli.

  Args:
    board (np.ndarray): The board matrix containg the information about:
      nullspaces, broccoli position and proximity
    board_object (Board): The object containing all of the information about the board
  Returns:
    array[int]: An array of [row, column] position of a broccoli
  """
  pos = [0,0]
  invalidPosition = True

  while invalidPosition:
    pos = [
      random.randrange(0, board_object.total_rows),
      random.randrange(0, board_object.total_columns)
      ]
    if board[pos[0], pos[1]] >= 0:
      invalidPosition = False
  
  return pos

def board_broccoli_filler(board_object, broccoli_amount=1):
  """Fills a board with a specific number of broccolis.

  Args:
    board_object (Board): The object containing all of the information about the board
    broccoli_amount (int): The number of broccolis on the board (default 1)
  Returns:
    Board: The board object with the board matrix filled the specified amount of broccolis
  """
  board = board_object.board
  total_rows = board_object.total_rows
  total_columns = board_object.total_columns

  if broccoli_amount >= board_object.available_space:
    broccoli_amount = board_object.available_space - 1

  for _ in range(broccoli_amount):
    pos = defineBroccoliPositions(board, board_object)
    board[pos[0], pos[1]] = -1
    board = broccoliProximity(board, pos, total_rows, total_columns)

  board_object.change_board(board)
  board_object.change_broccoli_amount(broccoli_amount)

  return board_object