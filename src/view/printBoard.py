import src.lang.language as Lg
from src.logic.handleMove import handle_move
from src.logic.constants.gameValues import get_game_over_text, get_winning_text, GAME_STATUS
from src.logic.constants.boardValues import GET_BOARD_VALUE
from src.logic.constants.styleValues import CONSOLE_NULLSPACE, CONSOLE_EMPTY_CHECKED_TILE, CONSOLE_EMPTY_UNCHECKED_TILE

def printing(board_object):
  """Handles the printing of the board on console.

  Args:
    board_object (Board): The object containing all of the information about the board
  """
  guide_row = "     "
  separation_row = "   --"
  for j in range(board_object.tiles_board.shape[1]):
    complement = "  "
    if j+1 >= 10:
      complement = " "

    guide_row += str(j + 1) + complement
    separation_row += "---"

  print(guide_row)
  print(separation_row)

  for i in range(board_object.tiles_board.shape[0]):
    complement = " "

    if i+1 >= 10:
      complement = ""

    row = complement + str(i + 1) + " | "
    for j in range(board_object.tiles_board[i].shape[0]):
      tile = board_object.tiles_board[i,j]
      tile_value = str(tile["tileValue"])
      checked = tile["checked"]

      if tile_value == str(GET_BOARD_VALUE["nullSpace"]):
        tile_value = CONSOLE_NULLSPACE

      if tile_value == str(GET_BOARD_VALUE["blankSpace"]):
        tile_value = CONSOLE_EMPTY_UNCHECKED_TILE

        if checked:
          tile_value = CONSOLE_EMPTY_CHECKED_TILE

      row += tile_value + "  "

    row += "| " + str(i + 1)
    print(row)

  print(separation_row)
  print(guide_row)

def print_board_on_console(board_object):
  """Prints the board on the console.

  Request the player to make the moves on the game.
  Upon losing or wining the game prints the corresponding message
  Args:
    board_object (Board): The object containing all of the information about the board
  """
  game_status = 0
  row_limit = board_object.total_rows
  column_limit = board_object.total_columns
  printing(board_object)

  while GAME_STATUS[game_status] == "Play":
    row = int(input(Lg.lang["InputRow"])) - 1
    column = int(input(Lg.lang["InputColumn"])) - 1

    if (row < 0 or
        row >= row_limit or
        column < 0 or
        column >= column_limit):
      print(Lg.lang["InvalidRowColumn"])
      continue

    board_object, game_status = handle_move(board_object, [row, column])
    printing(board_object)

  if GAME_STATUS[game_status] == "Win":
    print(get_winning_text())
  
  if GAME_STATUS[game_status] == "Game Over":
    print(get_game_over_text())