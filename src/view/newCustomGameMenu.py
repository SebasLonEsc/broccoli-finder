import tkinter as tk
from functools import partial
import math

import src.lang.language as Lg
from src.logic.board import board_generator
from src.logic.interfaceTools import center_window, close_interface, go_back, create_info_menu
from src.view.boardInterface import create_board_interface
from src.logic.constants.boardValues import BOARD_SIZE_VALUES
from src.logic.constants.gameValues import GAME_BROCCOLI_PERCENTS
from src.logic.constants.styleValues import BUTTON_COLOR, BUTTON_ACTIVE_COLOR

def validate_inputs(rows, columns, broccoli_amount):
  """Validates if the input values are valid values.

  Args:
    rows (int): Number of rows on the board
    columns (int): Number of columns on the board
    broccoli_amount (int): Number of broccolis on the board
  Returns:
    str: Message indicating if the inputs are valid.
      "The following values are invalid:" if all values are valid.
      "The following values are invalid:" + InputValue if a value is invalid.
      "Value is not numeric" if there is a non numeric value
  """
  try:
    error_text = Lg.lang["InputErrorText"]
    number_of_rows = int(rows.get())
    number_of_columns = int(columns.get())
    number_of_broccolis = int(broccoli_amount.get())
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    board_size_upper_limit = BOARD_SIZE_VALUES["Big"][1]
    broccoli_percent_limit = GAME_BROCCOLI_PERCENTS["Big"]["Hard"][1]
    broccoli_limit = math.ceil(number_of_rows
                               * number_of_columns
                               * broccoli_percent_limit)

    if number_of_rows < board_size_lower_limit:
      error_text += "\n" + Lg.lang["InvalidRowLowerLimit"] + str(board_size_lower_limit)

    if number_of_rows > board_size_upper_limit:
      error_text += "\n" + Lg.lang["InvalidRowUpperLimit"] + str(board_size_upper_limit)

    if number_of_columns < board_size_lower_limit:
      error_text += "\n" + Lg.lang["InvalidColumnLowerLimit"] + str(board_size_lower_limit)

    if number_of_columns > board_size_upper_limit:
      error_text += "\n"+ Lg.lang["InvalidColumnUpperLimit"] + str(board_size_upper_limit)
      
    if number_of_broccolis < 1:
      error_text += "\n" + Lg.lang["ZeroBroccolisError"]

    if (number_of_broccolis > broccoli_limit and
        error_text == Lg.lang["InputErrorText"]):
      error_text = (Lg.lang["BroccoliErrorLimit1"]
                    + str(broccoli_limit)
                    + "\n"
                    + Lg.lang["BroccoliErrorLimit2"])
    
    return error_text
  except ValueError:
    return Lg.lang["InvalidNumericValue"]

def create_new_game(root, rows, columns, broccoli_amount, error_label, create_new_game_view, go_back_func):
  """Closes the current window and creates the new game interface.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    rows (int): Number of rows on the board
    columns (int): Number of columns on the board
    broccoli_amount (int): Number of broccolis on the board
    error_label (tk.Label): The label widget to display an error message
    create_new_game_view (Func): The function that creates the current view/window.
      Used in the next view for the go_back function
    go_back_func (Func): The current go_back function.
      Used to go back to the previous view (In this case the main menu)
  """
  error_text = validate_inputs(rows, columns, broccoli_amount)

  if error_text != Lg.lang["InputErrorText"]:
    error_label.config(text=error_text)
    return
  
  number_of_rows = int(rows.get())
  number_of_columns = int(columns.get())
  number_of_broccolis = int(broccoli_amount.get())

  broccoli_percent_limit = GAME_BROCCOLI_PERCENTS["Big"]["Hard"][1]
  broccoli_amount_proportion = math.ceil(number_of_rows
                                         * number_of_columns
                                         * broccoli_percent_limit)

  if number_of_broccolis > broccoli_amount_proportion:
    error_text = (Lg.lang["TooManyBroccolisError"]
                 + str(broccoli_amount_proportion))
    error_label.config(text=error_text)
    return

  close_interface(root)
  board_object = board_generator(number_of_rows, number_of_columns, number_of_broccolis)
  create_board_interface(board_object, create_new_game_view, go_back_func)

def create_new_game_view(go_back_func, go_to_main_menu):
  """Creates the new game menu interface.

  Args:
    go_back_func (Func): The current go_back function.
      Used to go back to the previous view
    go_to_main_menu (Func): Function to go back to the main menu
  """
  window_min_width = 250
  window_min_height = 150
  window_max_width = 300
  window_max_height = 200

  root = tk.Tk()
  root.title(Lg.lang["GameTitle"])
  root.minsize(window_min_width, window_min_height)
  root.maxsize(window_max_width, window_max_height)
  center_window(root, window_min_width, window_min_height)

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  game_menu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label=Lg.lang["GameTabMenu"], menu=game_menu)
  game_menu.add_command(label=Lg.lang["NewGameLabel"], command=partial(go_back, root, go_back_func, go_to_main_menu))
  game_menu.add_command(label=Lg.lang["MainMenuLabel"], command=partial(go_back, root, go_to_main_menu))
  game_menu.add_separator()
  game_menu.add_command(label=Lg.lang["Exit"], command=partial(close_interface, root))
  create_info_menu(tk, menu)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(
    frame,
    text=Lg.lang["CustomGameTitle"],
    anchor="center").pack()

  board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
  board_size_upper_limit = BOARD_SIZE_VALUES["Big"][1]
  broccoli_percent_limit = GAME_BROCCOLI_PERCENTS["Big"]["Hard"][1]
  maximum_number_of_broccolis = math.floor(board_size_upper_limit
                                           * board_size_upper_limit
                                           * broccoli_percent_limit)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True, fill="x")
  tk.Label(frame, text=Lg.lang["InputRowNumber"]).pack(padx=10, side="left", expand=True)
  rows = tk.Spinbox(frame,
                    from_=board_size_lower_limit,
                    to=board_size_upper_limit
                    )
  rows.pack(side="left", pady=2, expand=True)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True, fill="x")
  tk.Label(frame, text=Lg.lang["InputColumnNumber"]).pack(side="left", expand=True)
  columns = tk.Spinbox(frame,
                       from_=board_size_lower_limit,
                       to=board_size_upper_limit
                       )
  columns.pack(side="left", pady=2, expand=True)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True, fill="x")
  tk.Label(frame, text=Lg.lang["InputBroccoliNumber"]).pack(padx=2, side="left", expand=True)
  broccoli_amount = tk.Spinbox(frame, from_=1, to=maximum_number_of_broccolis)
  broccoli_amount.pack(side="left", pady=2, expand=True)

  button_frame = tk.Frame(root)
  button_frame.pack(pady=[2,2], expand=True)
  error_text_frame = tk.Frame(root)
  error_text_frame.pack(pady=[2,2], expand=True)

  error_label = tk.Label(error_text_frame, text="", anchor="center")
  tk.Button(button_frame,
            activebackground=BUTTON_ACTIVE_COLOR,
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(create_new_game,
                            root,
                            rows,
                            columns,
                            broccoli_amount,
                            error_label,
                            go_back_func,
                            go_to_main_menu
                            ),
            justify="center",
            height=1,
            padx=4,
            pady=0,
            text=Lg.lang["PlayButton"],
            ).pack(pady=[4,2])
  
  error_label.pack()
  root.mainloop()