import tkinter as tk
from tkinter import ttk
from functools import partial
from pathlib import Path
from PIL import Image, ImageTk
import random
import math
from src.logic.interfaceTools import centerWindow, closeInterface, goBack
from src.logic.board import boardGenerator
from src.view.boardInterface import createBoardInterface
from src.logic.constants.boardValues import BOARDSIZEVALUES
from src.logic.constants.gameValues import GAMEDIFFICULTIES, GAMEBROCCOLIPERCENTS
from src.logic.constants.styleValues import BOARDBUTTONSIZES, BUTTONCOLOR, BUTTONACTIVECOLOR
from src.logic.constants.imagesPaths import BOARDSELECTORIMAGES
from src.view.newCustomGameMenu import createNewGameView

# Closes the current window and creates the custom game window
# Input:
#   root: the root windget, the current window that is being displayed
#   goBackFunc: Function to go back to the current view
#   previousGoBackfunc: Function to go back to the previous view
# Output:
#   Nothing
def openCustomGameView(root, goBackFunc, previousGoBackFunc):
  closeInterface(root)
  createNewGameView(goBackFunc, previousGoBackFunc)

# Closes the current window and creates the new game window
# Input:
#   root: the root windget, the current window that is being displayed
#   goBackFunc: Function to go back to the current view
#   previousGoBackfunc: Function to go back to the previous view
#   gameDifficulty: The game difficulty combobox
#   boardSize: The selected board size
# Output:
#   Nothing
def createGame(root, goBackFunc, previousGoBackFunc, difficulty, boardSize):
  gameDifficulty = difficulty.get()

  broccoliPercent = GAMEBROCCOLIPERCENTS[boardSize][gameDifficulty]
  boardSizes = BOARDSIZEVALUES[boardSize]

  rows = random.randint(boardSizes[0], boardSizes[1])
  columns = random.randint(boardSizes[0], boardSizes[1])
  boardSize = rows * columns
  broccoliLowerLimit = math.ceil(boardSize * broccoliPercent[0])
  broccoliUpperLimit = math.floor(boardSize * broccoliPercent[1])
  broccoliAmount = broccoliLowerLimit

  if broccoliLowerLimit != broccoliUpperLimit and broccoliLowerLimit < broccoliUpperLimit:
    broccoliAmount = random.randint(broccoliLowerLimit, broccoliUpperLimit)

  closeInterface(root)
  boardObject = boardGenerator(rows, columns, broccoliAmount)
  createBoardInterface(boardObject, goBackFunc, previousGoBackFunc)

# Creates a board size button
# Input:
#   root: the root windget, the current window that is being displayed
#   goBackFunc: Function to go back to the current view
#   previousGoBackfunc: Function to go back to the previous view
#   masterWidget: The widget where the button is being placed
#   gameDifficulty: The game difficulty combobox
#   boardSize: The selected board size
# Output:
#   Nothing
def createBoardSizeButton(root, goBackFunc, previousGoBackFunc, masterWidget, difficulty, size = "Small"):
  currentDir = Path(__file__).parent
  imageName = BOARDSELECTORIMAGES[size]
  imageSize = BOARDBUTTONSIZES[size]
  imagePath = currentDir.parent / "images" / imageName

  image = Image.open(imagePath)
  image = image.resize(imageSize, Image.Resampling.LANCZOS)
  boardImage = ImageTk.PhotoImage(image)
  
  button = tk.Button(masterWidget,
                      activebackground=BUTTONACTIVECOLOR,
                      anchor="center",
                      bd=1,
                      bg=BUTTONCOLOR,
                      command= partial(createGame, root, goBackFunc, previousGoBackFunc, difficulty, size),
                      justify="center",
                      width=imageSize[0]+10,
                      height=imageSize[1]+20,
                      padx=4,
                      pady=0,
                      text=size,
                      image=boardImage,
                      compound="bottom"
  )
  button.image = boardImage
  
  return button

# Creates the new game selector menu interface
# Input:
#   goBackFunc: The current goBack function. Used to go back to the previous view (In this case the main menu)
# Output:
#   Nothing
def newGameMenu(goBackFunc):
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
                                values=GAMEDIFFICULTIES,
                                state="readonly")
  gameDifficulty.pack(side="left", padx=[2,4])
  gameDifficulty.set(GAMEDIFFICULTIES[0])

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  createBoardSizeButton(root, newGameMenu, goBackFunc, frame, gameDifficulty, "Small").pack(side="left", padx=[4,4], anchor="n")
  createBoardSizeButton(root, newGameMenu, goBackFunc, frame, gameDifficulty, "Medium").pack(side="left", padx=[4,4], anchor="n")
  createBoardSizeButton(root, newGameMenu, goBackFunc, frame, gameDifficulty, "Big").pack(side="left", padx=[4,4], anchor="n")

  frame = tk.Frame(root)
  frame.pack(pady=[8,2], expand=True)
  tk.Button(frame,
            activebackground="white",
            anchor="center",
            bd=1,
            bg=BUTTONCOLOR,
            command= partial(openCustomGameView, root, newGameMenu, goBackFunc),
            justify="center",
            height=1,
            width=10,
            padx=4,
            pady=0,
            text="Custom Game"
  ).pack(pady=[0,4])

  root.mainloop()
