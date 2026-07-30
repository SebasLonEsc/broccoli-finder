import tkinter as tk
from functools import partial
import math

from src.logic.board import boardGenerator
from src.logic.interfaceTools import centerWindow, closeInterface, goBack, createInfoMenu
from src.view.boardInterface import createBoardInterface
from src.logic.constants.boardValues import BOARDSIZEVALUES
from src.logic.constants.gameValues import GAMEBROCCOLIPERCENTS
from src.logic.constants.styleValues import BUTTONCOLOR, BUTTONACTIVECOLOR

def validateInputs(rows, columns, broccoliAmount):
  """Validates if the input values are valid values.

  Args:
    rows (int): Number of rows on the board
    columns (int): Number of columns on the board
    broccoliAmount (int): Number of broccolis on the board
  Returns:
    str: Message indicating if the inputs are valid.
      "The following values are invalid:" if all values are valid.
      "The following values are invalid:" + InputValue if a value is invalid.
      "Value is not numeric" if there is a non numeric value
  """
  try:
    errorText = "The following values are invalid:"
    numberOfRows = int(rows.get())
    numberOfColumns = int(columns.get())
    numberOfBroccolis = int(broccoliAmount.get())
    boardSizeLowerLimit = BOARDSIZEVALUES["Small"][0]
    boardSizeUpperLimit = BOARDSIZEVALUES["Big"][1]
    broccoliPercentLimit = GAMEBROCCOLIPERCENTS["Big"]["Hard"][1]
    broccoliLimit = math.ceil(numberOfRows
                              * numberOfColumns
                              * broccoliPercentLimit)

    if numberOfRows < boardSizeLowerLimit:
      errorText += "\n# Rows can't be less than " + str(boardSizeLowerLimit)

    if numberOfRows > boardSizeUpperLimit:
      errorText += "\n# Rows can't be more than " + str(boardSizeUpperLimit)

    if numberOfColumns < boardSizeLowerLimit:
      errorText += "\n# Columns can't be less than " + str(boardSizeLowerLimit)

    if numberOfColumns > boardSizeUpperLimit:
      errorText += "\n# Columns can't be more than " + str(boardSizeUpperLimit)
      
    if numberOfBroccolis < 1:
      errorText += "\n# Broccolis can't be less than 1"

    if (numberOfBroccolis > broccoliLimit and
        errorText == "The following values are invalid:"):
      errorText = ("Number of Broccolis can't be more than "
                   + str(broccoliLimit)
                   + "\nfor the current board size")
    
    return errorText
  except:
    return "Value is not numeric"

def createNewGame(root, rows, columns, broccoliAmount, errorLabel, createNewGameView, goBackFunc):
  """Closes the current window and creates the new game interface.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    rows (int): Number of rows on the board
    columns (int): Number of columns on the board
    broccoliAmount (int): Number of broccolis on the board
    errorLabel (tk.Label): The label widget to display an error message
    createNewGameView (Func): The function that creates the current view/window.
      Used in the next view for the goBack function
    goBackFunc (Func): The current goBack function.
      Used to go back to the previous view (In this case the main menu)
  """
  errorText = validateInputs(rows, columns, broccoliAmount)

  if errorText != "The following values are invalid:":
    errorLabel.config(text=errorText)
    return
  
  numberOfRows = int(rows.get())
  numberOfColumns = int(columns.get())
  numberOfBroccolis = int(broccoliAmount.get())

  broccoliPercentLimit = GAMEBROCCOLIPERCENTS["Big"]["Hard"][1]
  broccoliAmountProportion = math.ceil(numberOfRows
                                       * numberOfColumns
                                       * broccoliPercentLimit)

  if numberOfBroccolis > broccoliAmountProportion:
    errorText = ("Please reduce the amount of Broccolis to no more than "
                 + str(broccoliAmountProportion))
    errorLabel.config(text=errorText)
    return

  closeInterface(root)
  boardObject = boardGenerator(numberOfRows, numberOfColumns, numberOfBroccolis)
  createBoardInterface(boardObject, createNewGameView, goBackFunc)

def createNewGameView(goBackFunc, goToMainMenu):
  """Creates the new game menu interface.

  Args:
    goBackFunc (Func): The current goBack function.
      Used to go back to the previous view
    goToMainMenu (Func): Function to go back to the main menu
  """
  windowMinWidth = 250
  windowMinHeight = 150
  windowMaxWidth = 300
  windowMaxHeight = 200

  root = tk.Tk()
  root.title("New Game")
  root.minsize(windowMinWidth, windowMinHeight)
  root.maxsize(windowMaxWidth, windowMaxHeight)
  centerWindow(root, windowMinWidth, windowMinHeight)

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  gameMenu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label="Game", menu=gameMenu)
  gameMenu.add_command(label="New Game", command=partial(goBack, root, goBackFunc, goToMainMenu))
  gameMenu.add_command(label="Main Menu", command=partial(goBack, root, goToMainMenu))
  gameMenu.add_separator()
  gameMenu.add_command(label="Exit", command=partial(closeInterface, root))
  createInfoMenu(tk, menu)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(
    frame,
    text="Customize your Game",
    anchor="center").pack()

  boardSizeLowerLimit = BOARDSIZEVALUES["Small"][0]
  boardSizeUpperLimit = BOARDSIZEVALUES["Big"][1]
  broccoliPercentLimit = GAMEBROCCOLIPERCENTS["Big"]["Hard"][1]
  maximumNumberOfBroccolis = math.floor(boardSizeUpperLimit
                                        * boardSizeUpperLimit
                                        * broccoliPercentLimit)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(frame, text="# Rows").pack(side="left", padx=[0,20])
  rows = tk.Spinbox(frame,
                    from_=boardSizeLowerLimit,
                    to=boardSizeUpperLimit
                    )
  rows.pack(side="left", pady=2)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(frame, text="# Columns").pack(side="left")
  columns = tk.Spinbox(frame,
                       from_=boardSizeLowerLimit,
                       to=boardSizeUpperLimit
                       )
  columns.pack(side="left", pady=2)

  frame = tk.Frame(root)
  frame.pack(pady=[2,2], expand=True)
  tk.Label(frame, text="# Broccolis").pack(side="left")
  broccoliAmount = tk.Spinbox(frame, from_=1, to=maximumNumberOfBroccolis)
  broccoliAmount.pack(side="left", pady=2)

  buttonFrame = tk.Frame(root)
  buttonFrame.pack(pady=[2,2], expand=True)
  errorTextFrame = tk.Frame(root)
  errorTextFrame.pack(pady=[2,2], expand=True)

  errorLabel = tk.Label(errorTextFrame, text="", anchor="center")
  tk.Button(buttonFrame,
            activebackground=BUTTONACTIVECOLOR,
            anchor="center",
            bd=1,
            bg=BUTTONCOLOR,
            command=partial(createNewGame,
                            root,
                            rows,
                            columns,
                            broccoliAmount,
                            errorLabel,
                            goBackFunc,
                            goToMainMenu
                            ),
            justify="center",
            height=1,
            padx=4,
            pady=0,
            text="Play",
            ).pack(pady=[4,2])
  
  errorLabel.pack()
  root.mainloop()