import tkinter as tk
from tkinter import ttk
from functools import partial
from pathlib import Path
import random
import math
from PIL import Image, ImageTk

from src.logic.interfaceTools import centerWindow, closeInterface, goBack, createInfoMenu
from src.logic.board import board_generator
from src.view.boardInterface import createBoardInterface
from src.view.newCustomGameMenu import createNewGameView
from src.logic.constants.boardValues import BOARD_SIZE_VALUES, BOARD_SIZES
from src.logic.constants.gameValues import GAME_DIFFICULTIES, GAME_BROCCOLI_PERCENTS
from src.logic.constants.styleValues import BOARD_BUTTON_SIZES, BUTTON_COLOR, BUTTON_ACTIVE_COLOR
from src.logic.constants.imagesPaths import BOARD_SELECTOR_IMAGES

def openCustomGameView(root, goBackFunc, previousGoBackFunc):
  """Closes the current window and creates the custom game window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    goBackFunc (func): Function to go back to the current view
    previousGoBackfunc (func): Function to go back to the previous view
  """
  closeInterface(root)
  createNewGameView(goBackFunc, previousGoBackFunc)

def createGame(root, goBackFunc, previousGoBackFunc, difficulty, board_size):
  """Closes the current window and creates the new game window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    goBackFunc (Func): Function to go back to the current view
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

  closeInterface(root)
  boardObject = board_generator(rows, columns, broccoli_amount)
  createBoardInterface(boardObject, goBackFunc, previousGoBackFunc)

def createBoardSizeButton(root, goBackFunc, previousGoBackFunc, masterWidget, difficulty, size = "Small"):
  """Creates a board size selector button.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    goBackFunc (Func): Function to go back to the current view
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
                                     goBackFunc,
                                     previousGoBackFunc,
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

def newGameMenu(goBackFunc):
  """Creates the new game selector menu interface.

  Args:
    goBackFunc (Func): The current goBack function.
      Used to go back to the previous view (In this case the main menu)
  """
  windowWidth = 786
  windowHeight = 380

  root = tk.Tk()
  root.title("New Game")
  root.minsize(windowWidth, windowHeight)
  centerWindow(root, windowWidth, windowHeight)

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  gameMenu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label="Game", menu=gameMenu)
  gameMenu.add_command(label="Main Menu", command=partial(goBack, root, goBackFunc))
  gameMenu.add_separator()
  gameMenu.add_command(label="Exit", command=partial(closeInterface, root))
  createInfoMenu(tk, menu)

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
                          goBackFunc,
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
                            goBackFunc
                            ),
            justify="center",
            height=1,
            width=10,
            padx=4,
            pady=0,
            text="Custom Game"
            ).pack(pady=[0,4])

  root.mainloop()
