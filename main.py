from src.view.printBoard import print_board_on_console
from src.view.mainMenuView import create_main_menu_view
from src.logic.board import board_generator

def select_game_type(game_type):
  """Handles the generation of the Board and redirects to the specific game interface.

  Args:
    game_type (int): The type of interface used for the game
      1 -> Play the game in console
      2 -> Play the game in an interface
  """
  if game_type == 1:
    rows = int(input("Enter the rows:"))
    columns = int(input("Enter the columns:"))
    broccoli_amount = int(input("Enter the number of broccolis:"))
    board_object = board_generator(rows, columns, broccoli_amount)
    print_board_on_console(board_object)

  else:
    create_main_menu_view()

def main():
  invalid_game_type = True
  game_type = -1

  while(invalid_game_type):
    print("-------------------")
    print("Select a game type:")
    print("1: console game")
    print("2: interface game")
    print("-------------------")
    game_type = int(input("Enter the game type:"))

    if game_type == 1 or game_type == 2:
      invalid_game_type = False
    else:
      print("\nInvalid game type")

  select_game_type(game_type)

main()