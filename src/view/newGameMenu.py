import tkinter as tk
from tkinter import ttk
from functools import partial
import random
import math
from src.logic.interfaceTools import centerWindow, closeInterface, goBack
from src.logic.board import boardGenerator
from src.view.boardInterface import createBoardInterface
from src.logic.constants.boardValues import BOARDSIZEVALUES
from src.logic.constants.gameValues import GAMEDIFFICULTIES, GAMEBROCCOLIPERCENTS

# Closes the current window and creates the new game window
# Input:
#   root: the root windget, the current window that is being displayed
#   previousGoBackfunc: Function to go back to the previous view
#   goBackFunc: Function to go back to the current view
#   gameDifficulty: The selected game difficulty
#   boardSize: The selected board size
# Output:
#   Nothing
def createGame(root, previousGoBackFunc, goBackFunc, gameDifficulty, boardSize):
  broccoliPercent = GAMEBROCCOLIPERCENTS[gameDifficulty]
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

def createGameSelectorButton(root, goBackFunc, previousGoBackFunc, masterWidget, difficulty, size = "Small"):
  gameDifficulty = difficulty.get()
  
  button = tk.Button(masterWidget,
                      activebackground="white",
                      anchor="center",
                      bd=1,
                      bg="lightgray",
                      command= partial(createGame, root, previousGoBackFunc, goBackFunc, gameDifficulty, size),
                      disabledforeground="white",
                      justify="center",
                      height=1,
                      padx=4,
                      pady=0,
                      text=size,
                      )
  
  return button

# Creates the new game selector menu interface
# Input:
#   goBackFunc: The current goBack function. Used to go back to the previous view (In this case the main menu)
# Output:
#   Nothing
def newGameMenu(goBackFunc):
  windowWidth = 210
  windowHeight = 140

  root = tk.Tk()
  root.title("New Game")
  root.minsize(windowWidth, windowHeight)
  root.maxsize(windowWidth, windowHeight)
  centerWindow(root, windowWidth, windowHeight)

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  gameMenu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label="Game", menu=gameMenu)
  gameMenu.add_command(label="Main Menu", command=partial(goBack, root, goBackFunc))
  gameMenu.add_separator()
  gameMenu.add_command(label="Exit", command=partial(closeInterface, root))

  frame = tk.Frame(root)
  frame.grid(row=0, pady=[2,2])
  tk.Label(
    frame,
    text="New Game",
    anchor="center").grid(row=0)
  
  frame = tk.Frame(root)
  frame.grid(row=1, pady=[2,2])
  tk.Label(
    frame,
    text="Difficulty",
    anchor="center").grid(row=0, column=1, padx=[2,2])
  gameDifficulty = ttk.Combobox(frame,
                                values=GAMEDIFFICULTIES,
                                state="readonly")
  gameDifficulty.grid(row=0, column=2, padx=[2,2])
  gameDifficulty.set(GAMEDIFFICULTIES[0])

  frame = tk.Frame(root)
  frame.grid(row=2, pady=[2,2])
  createGameSelectorButton(root, newGameMenu, goBackFunc, frame, gameDifficulty, "Small").grid(row=0, column=0, padx=[4,4])
  createGameSelectorButton(root, newGameMenu, goBackFunc, frame, gameDifficulty, "Medium").grid(row=0, column=1, padx=[4,4])
  createGameSelectorButton(root, newGameMenu, goBackFunc, frame, gameDifficulty, "Big").grid(row=0, column=2, padx=[4,4])

  root.mainloop()
