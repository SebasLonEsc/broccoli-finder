import tkinter as tk
from functools import partial
import math
from src.logic.board import boardGenerator
from src.view.boardInterface import createBoardInterface

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

def createNewGame(root, rows, columns, broccoliAmount, errorLabel):
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

  root.destroy()
  boardObject = boardGenerator(numberOfRows, numberOfColumns, numberOfBroccolis)
  createBoardInterface(boardObject)

def createNewGameView():
  root = tk.Tk()
  root.title("Broccolis")
  tk.Label(
    root,
    text="New Game",
    anchor="center").grid(row=0)
  
  tk.Label(root, text="# Rows").grid(row=2, column=0)
  tk.Label(root, text="# Columns").grid(row=3, column=0)
  tk.Label(root, text="# Broccolis").grid(row=4, column=0)
  errorLabel = tk.Label(root, text="", anchor="center")

  rows = tk.Spinbox(root, from_=2, to=30)
  columns = tk.Spinbox(root, from_=2, to=30)
  broccoliAmount = tk.Spinbox(root, from_=1, to=40)

  rows.grid(row=2, column=1)
  columns.grid(row=3, column=1)
  broccoliAmount.grid(row=4, column=1)

  tk.Button(root,
            activebackground="white",
            anchor="center",
            bd=1,
            bg="lightgray",
            command= partial(createNewGame, root, rows, columns, broccoliAmount, errorLabel),
            disabledforeground="white",
            justify="center",
            height=1,
            width=3,
            padx=0,
            pady=0,
            text= "Play",
            ).grid(row=5)
  
  errorLabel.grid(row=6)
  root.mainloop()