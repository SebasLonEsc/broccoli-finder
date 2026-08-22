import tkinter as tk
from tkinter import ttk
from functools import partial
from pathlib import Path
import random
import math
from PIL import Image, ImageTk

import src.lang.language as Lg
from src.logic.interfaceTools import center_window, close_interface, create_menu
from src.logic.board import board_generator
from src.view.boardInterface import create_board_interface
from src.view.newCustomGameMenu import create_new_game_view
from src.logic.constants.boardValues import BOARD_SIZE_VALUES, BOARD_SIZES
from src.logic.constants.gameValues import GAME_BROCCOLI_PERCENTS
from src.logic.constants.styleValues import BOARD_BUTTON_SIZES, BUTTON_COLOR, BUTTON_ACTIVE_COLOR
from src.logic.constants.imagesPaths import BOARD_SELECTOR_IMAGES, IMAGES_FOLDER

def open_custom_game_view(root, go_back_func, previous_go_back_func):
  """Closes the current window and creates the custom game window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (func): Function to go back to the current view
    previous_go_back_func (func): Function to go back to the previous view
  """
  close_interface(root)
  create_new_game_view(go_back_func, previous_go_back_func)

def create_game(root, go_back_func, previous_go_back_func, difficulty, board_size):
  """Closes the current window and creates the new game window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (Func): Function to go back to the current view
    previous_go_back_func (Func): Function to go back to the previous view
    difficulty (int): The game difficulty combobox
    board_size (str): The selected board size
  """
  game_difficulty = Lg.lang[difficulty.get()]

  broccoli_percent = GAME_BROCCOLI_PERCENTS[board_size][game_difficulty]
  board_sizes = BOARD_SIZE_VALUES[board_size]

  rows = random.randint(board_sizes[0], board_sizes[1])
  columns = random.randint(board_sizes[0], board_sizes[1])
  board_size = rows * columns
  broccoli_lower_limit = math.ceil(board_size * broccoli_percent[0])
  broccoli_upper_limit = math.floor(board_size * broccoli_percent[1])
  broccoli_amount = broccoli_lower_limit

  if (broccoli_lower_limit != broccoli_upper_limit and
      broccoli_lower_limit < broccoli_upper_limit):
    broccoli_amount = random.randint(broccoli_lower_limit, broccoli_upper_limit)

  close_interface(root)
  board_object = board_generator(rows, columns, broccoli_amount)
  create_board_interface(board_object, go_back_func, previous_go_back_func)

def create_board_size_selector_button(root, go_back_func, previous_go_back_func, master_widget, difficulty, size = "Small"):
  """Creates a board size selector button.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (Func): Function to go back to the current view
    previous_go_back_func (Func): Function to go back to the previous view
    master_widget (tk.Widget): The widget where the button is being placed
    difficulty (int): The game difficulty combobox
    board_size (str): The selected board size
  """
  current_dir = Path(__file__).parent
  image_name = BOARD_SELECTOR_IMAGES[size]
  image_size = BOARD_BUTTON_SIZES[size]
  image_path = current_dir.parent / IMAGES_FOLDER / image_name

  image = Image.open(image_path)
  image = image.resize(image_size, Image.Resampling.LANCZOS)
  board_image = ImageTk.PhotoImage(image)
  
  button = tk.Button(master_widget,
                     activebackground=BUTTON_ACTIVE_COLOR,
                     anchor="center",
                     bd=1,
                     bg=BUTTON_COLOR,
                     command=partial(create_game,
                                     root,
                                     go_back_func,
                                     previous_go_back_func,
                                     difficulty,
                                     size
                                     ),
                     justify="center",
                     width=image_size[0] + 10, # Increasing space for text
                     height=image_size[1] + 20, # Increasing space for text
                     padx=4,
                     pady=0,
                     text=Lg.lang[size],
                     image=board_image,
                     compound="bottom"
                     )
  button.image = board_image
  
  return button

def new_game_menu(go_back_func):
  """Creates the new game selector menu interface.

  Args:
    go_back_func (Func): The current go_back function.
      Used to go back to the previous view (In this case the main menu)
  """
  window_width = 786
  window_height = 380

  root = tk.Tk()
  root.title(Lg.lang["GameTitle"])
  root.minsize(window_width, window_height)
  center_window(root, window_width, window_height)

  create_menu(root=root,
              add_main_menu_shortcut=True,
              main_menu_shortcut=go_back_func,
              add_info_menu=True,
              add_help_menu=True)

  frame = tk.Frame(root)
  frame.pack(pady=2, expand=True)
  tk.Label(frame,
           text=Lg.lang["NewGame"],
           anchor="center").pack()
  
  frame = tk.Frame(root)
  frame.pack(pady=2, expand=True)
  tk.Label(frame,
           text=Lg.lang["Difficulty"],
           anchor="center"
           ).pack(side="left", padx=2)
  
  game_difficulty = ttk.Combobox(frame,
                                 values=Lg.lang["GameDifficulties"],
                                 state="readonly")
  game_difficulty.pack(side="left", padx=[2,4])
  game_difficulty.set(Lg.lang["GameDifficulties"][0])

  frame = tk.Frame(root)
  frame.pack(pady=2, expand=True)

  for size in BOARD_SIZES:
    create_board_size_selector_button(root,
                                      new_game_menu,
                                      go_back_func,
                                      frame,
                                      game_difficulty,
                                      size
                                      ).pack(side="left", padx=4, anchor="n")

  frame = tk.Frame(root)
  frame.pack(pady=[8,2], expand=True)
  tk.Button(frame,
            activebackground=BUTTON_ACTIVE_COLOR,
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(open_custom_game_view,
                            root,
                            new_game_menu,
                            go_back_func
                            ),
            justify="center",
            height=1,
            width=10,
            padx=4,
            pady=0,
            text=Lg.lang["CustomGameButton"]
            ).pack(pady=[0,4])

  root.mainloop()
