import random

from .broccoliProximity import broccoli_proximity, update_proximity_numbers_for_rainbow_broccoli
from src.logic.constants.gameValues import RAINBOW_BROCCOLI_PROPORTION_CHANCES, RAINBOW_BROCCOLI_PERCENT

def validate_rainbow_broccoli_chance(broccoli_proportion, broccoli_amount):
  """Validates at random to add or not a rainbow broccoli

  Args:
    broccoli_proportion (float): The percentage of broccolis in the available space
    broccoli_amount (int): The amoun of broccolis on the board
  Returns:
    bool: True to add rainbow broccoli, false otherwise
  """
  if broccoli_amount == 1:
    return False

  for i in range(len(RAINBOW_BROCCOLI_PROPORTION_CHANCES)):
    if (broccoli_proportion >= RAINBOW_BROCCOLI_PROPORTION_CHANCES[i][0] and
        broccoli_proportion <= RAINBOW_BROCCOLI_PROPORTION_CHANCES[i][1]):
      return random.random() <= RAINBOW_BROCCOLI_PERCENT[i]

  return False

def add_rainbow_broccoli(board, broccoli_positions, total_rows, total_columns):
  """Adds the rainbow broccoli to the board

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    broccoli_positions (array[array[int,int]]): The positions of the broccolis
    total_rows (int): The amount of rows on the board
    total_columns (int): The amount of columns on the board
  Returns:
    np.ndarray: The board matrix with the proximity numbers.
      Which indicate the amount of broccolis next to each tile
  """
  pos = broccoli_positions[0]

  if len(broccoli_positions) > 1:
    array_position = random.randrange(0, len(broccoli_positions))
    pos = broccoli_positions[array_position]

  board[pos[0], pos[1]] = -3
  board = update_proximity_numbers_for_rainbow_broccoli(board, pos, total_rows, total_columns)

  return board

def define_broccoli_positions(board, board_object):
  """Calculates a valid random position for a broccoli.

  Args:
    board (np.ndarray): The board matrix containg the information about:
      nullspaces, broccoli position and proximity
    board_object (Board): The object containing all of the information about the board
  Returns:
    array[int]: An array of [row, column] position of a broccoli
  """
  pos = [0,0]
  invalid_position = True

  while invalid_position:
    pos = [
      random.randrange(0, board_object.total_rows),
      random.randrange(0, board_object.total_columns)
      ]
    if board[pos[0], pos[1]] >= 0:
      invalid_position = False
  
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
    pos = define_broccoli_positions(board, board_object)
    board[pos[0], pos[1]] = -1
    board_object.add_broccoli_positions(pos)
    board = broccoli_proximity(board, pos, total_rows, total_columns)

  broccoli_proportion = broccoli_amount / board_object.available_space
  generate_rainbow_broccoli = validate_rainbow_broccoli_chance(broccoli_proportion, broccoli_amount)
  if generate_rainbow_broccoli:
    board = add_rainbow_broccoli(board, board_object.broccoli_positions, total_rows, total_columns)

  board_object.change_board(board)
  board_object.change_broccoli_amount(broccoli_amount)

  return board_object