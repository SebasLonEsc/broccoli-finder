import tkinter as tk
from tkinter import ttk
from functools import partial
from pathlib import Path
import random
import math
from PIL import Image, ImageTk

from src.logic.interfaceTools import center_window, close_interface, go_back, create_info_menu
from src.logic.board import board_generator
from src.view.boardInterface import createBoardInterface
from src.view.newCustomGameMenu import createNewGameView
from src.logic.constants.boardValues import BOARD_SIZE_VALUES, BOARD_SIZES
from src.logic.constants.gameValues import GAME_DIFFICULTIES, GAME_BROCCOLI_PERCENTS
from src.logic.constants.styleValues import BOARD_BUTTON_SIZES, BUTTON_COLOR, BUTTON_ACTIVE_COLOR
from src.logic.constants.imagesPaths import BOARD_SELECTOR_IMAGES

def openCustomGameView(root, go_back_func, previous_go_back_func):
  """Closes the current window and creates the custom game window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (func): Function to go back to the current view
    previousGoBackfunc (func): Function to go back to the previous view
  """
  close_interface(root)
  createNewGameView(go_back_func, previous_go_back_func)

def createGame(root, go_back_func, previous_go_back_func, difficulty, board_size):
  """Closes the current window and creates the new game window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (Func): Function to go back to the current view
    previousGoBackfunc (Func): Function to go back to the previous view
    gameDifficulty (int): The game difficulty combobox
    board_size (str): The selected board size
  """
  gameDifficulty = difficulty.get()

  broccoliPercent = GAME_BROCCOLI_PERCENTS[board_size][gameDifficulty]
  board_sizes = BOARD_SIZE_VALUES[board_size]

  rows = random.randint(board_sizes[0], board_sizes[1])
  columns = random.randint(board_sizes[0], board_sizes[1])
  board_size = rows * columns
  broccoliLowerLimit = math.ceil(board_size * broccoliPercent[0])
  broccoliUpperLimit = math.floor(board_size * broccoliPercent[1])
  broccoli_amount = broccoliLowerLimit

  if (broccoliLowerLimit != broccoliUpperLimit and
      broccoliLowerLimit < broccoliUpperLimit):
    broccoli_amount = random.randint(broccoliLowerLimit, broccoliUpperLimit)

  close_interface(root)
  boardObject = board_generator(rows, columns, broccoli_amount)
  createBoardInterface(boardObject, go_back_func, previous_go_back_func)

def createBoardSizeButton(root, go_back_func, previous_go_back_func, masterWidget, difficulty, size = "Small"):
  """Creates a board size selector button.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (Func): Function to go back to the current view
    previousGoBackfunc (Func): Function to go back to the previous view
    masterWidget (tk.Widget): The widget where the button is being placed
    gameDifficulty (int): The game difficulty combobox
    board_size (str): The selected board size
  """
  currentDir = Path(__file__).parent
  imageName = BOARD_SELECTOR_IMAGES[size]
  imageSize = BOARD_BUTTON_SIZES[size]
  imagePath = currentDir.parent / "images" / imageName

  image = Image.open(imagePath)
  image = image.resize(imageSize, Image.Resampling.LANCZOS)
  boardImage = ImageTk.PhotoImage(image)
  
  button = tk.Button(masterWidget,
                     activebackground=BUTTON_ACTIVE_COLOR,
                     anchor="center",
                     bd=1,
                     bg=BUTTON_COLOR,
                     command=partial(createGame,
                                     root,
                                     go_back_func,
                                     previous_go_back_func,
                                     difficulty,
                                     size
                                     ),
                     justify="center",
                     width=imageSize[0] + 10, #Leave space for padding
                     height=imageSize[1] + 20, #Leave space for padding
                     padx=4,
                     pady=0,
                     text=size,
                     image=boardImage,
                     compound="bottom"
                     )
  button.image = boardImage
  
  return button

def newGameMenu(go_back_func):
  """Creates the new game selector menu interface.

  Args:
    go_back_func (Func): The current go_back function.
      Used to go back to the previous view (In this case the main menu)
  """
  window_width = 786
  window_height = 380

  root = tk.Tk()
  root.title("New Game")
  root.minsize(window_width, window_height)
  center_window(root, window_width, window_height)

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  gameMenu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label="Game", menu=gameMenu)
  gameMenu.add_command(label="Main Menu", command=partial(go_back, root, go_back_func))
  gameMenu.add_separator()
  gameMenu.add_command(label="Exit", command=partial(close_interface, root))
  create_info_menu(tk, menu)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(
    frame,
    text="New Game",
    anchor="center").pack()
  
  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(
    frame,
    text="Difficulty",
    anchor="center").pack(side="left", padx=[2,2])
  gameDifficulty = ttk.Combobox(frame,
                                values=GAME_DIFFICULTIES,
                                state="readonly")
  gameDifficulty.pack(side="left", padx=[2,4])
  gameDifficulty.set(GAME_DIFFICULTIES[0])

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)

  for size in BOARD_SIZES:
    createBoardSizeButton(root,
                          newGameMenu,
                          go_back_func,
                          frame,
                          gameDifficulty,
                          size
                          ).pack(side="left", padx=[4,4], anchor="n")

  frame = tk.Frame(root)
  frame.pack(pady=[8,2], expand=True)
  tk.Button(frame,
            activebackground="white",
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(openCustomGameView,
                            root,
                            newGameMenu,
                            go_back_func
                            ),
            justify="center",
            height=1,
            width=10,
            padx=4,
            pady=0,
            text="Custom Game"
            ).pack(pady=[0,4])

  root.mainloop()
