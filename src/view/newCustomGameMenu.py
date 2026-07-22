import tkinter as tk
from functools import partial
import math
from src.logic.board import boardGenerator
from src.logic.interfaceTools import centerWindow, closeInterface, goBack
from src.view.boardInterface import createBoardInterface

# Validates if the input values are valid values
# Input:
#   rows: number of rows on the board
#   columns: number of columns on the board
#   broccoliAmount: number of broccolis on the board
# Output:
#   Returns a String depending if the inputs are valid
#     "The following values are invalid:" if all values are valid
#     "The following values are invalid:" + InputValue if one/several value is invalid
#     "Value is not numeric" if there is a non numeric value
def validateInputs(rows, columns, broccoliAmount):
  try:
    errorText = "The following values are invalid:"
    numberOfRows = int(rows.get())
    numberOfColumns = int(columns.get())
    numberOfBroccolis = int(broccoliAmount.get())

    if type(numberOfRows) is not int:
      errorText += "\n# Rows"

    if type(numberOfColumns) is not int:
      errorText += "\n# Columns"
      
    if type(numberOfBroccolis) is not int:
      errorText += "\n# Broccolis"
    
    return errorText
  except:
    return "Value is not numeric"

# Closes the current window and creates the new game interface
# Input:
#   root: the root windget, the current window that is being displayed
#   rows: number of rows on the board
#   columns: number of columns on the board
#   broccoliAmount: number of broccolis on the board
#   errorLabel: The label widget to display an error message
#   createNewGameView: The function that creates the current view/window. Used in the next view for the goBack function
#   goBackFunc: The current goBack function. Used to go back to the previous view (In this case the main menu)
# Output:
#   Nothing
def createNewGame(root, rows, columns, broccoliAmount, errorLabel, createNewGameView, goBackFunc):
  errorText = validateInputs(rows, columns, broccoliAmount)

  if errorText != "The following values are invalid:":
    errorLabel.config(text=errorText)
    return
  
  numberOfRows = int(rows.get())
  numberOfColumns = int(columns.get())
  numberOfBroccolis = int(broccoliAmount.get())

  broccoliAmountProportion = math.floor(numberOfRows * numberOfColumns * 0.3)

  if numberOfBroccolis > broccoliAmountProportion:
    errorLabel.config(text="Please reduce the amount of Broccolis")
    return

  closeInterface(root)
  boardObject = boardGenerator(numberOfRows, numberOfColumns, numberOfBroccolis)
  createBoardInterface(boardObject, createNewGameView, goBackFunc)

# Creates the new game menu interface
# Input:
#   goBackFunc: The current goBack function. Used to go back to the previous view (In this case the main menu)
# Output:
#   Nothing
def createNewGameView(goBackFunc):
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

  tk.Label(
    root,
    text="New Game",
    anchor="center").grid(row=0, columnspan=4)
  
  tk.Label(root, text="# Rows").grid(row=2, column=1, columnspan=1)
  tk.Label(root, text="# Columns").grid(row=3, column=1, columnspan=1)
  tk.Label(root, text="# Broccolis").grid(row=4, column=1, columnspan=1)
  errorLabel = tk.Label(root, text="", anchor="center")

  rows = tk.Spinbox(root, from_=2, to=30)
  columns = tk.Spinbox(root, from_=2, to=30)
  broccoliAmount = tk.Spinbox(root, from_=1, to=40)

  rows.grid(row=2, column=2, columnspan=1, pady=2)
  columns.grid(row=3, column=2, columnspan=1, pady=2)
  broccoliAmount.grid(row=4, column=2, columnspan=1, pady=2)

  tk.Button(root,
            activebackground="white",
            anchor="center",
            bd=1,
            bg="lightgray",
            command= partial(createNewGame, root, rows, columns, broccoliAmount, errorLabel, createNewGameView, goBackFunc),
            disabledforeground="white",
            justify="center",
            height=1,
            padx=4,
            pady=0,
            text= "Play",
            ).grid(row=5, column=1, columnspan=2, pady=[4,2])
  
  errorLabel.grid(row=6, columnspan=4)
  root.mainloop()