import tkinter as tk
from functools import partial
import numpy as np
from src.logic.handleMove import handleMove

def handleText(boardObject, buttons):
  tilesBoard = boardObject.tilesBoard

  for row in range(0, boardObject.totalRows):
    for column in range(0, boardObject.totalColumns):
      buttonText = buttons[row, column].cget("text")
      print(buttonText)

      if buttonText != "":
        continue

      text = tilesBoard[row, column]["tileValue"]
      checked = tilesBoard[row, column]["checked"]

      if checked:
        print(row, column)
        buttons[row, column].config(text=text)

def handleClick(boardObject, buttons, movePosition):
  boardObject, gameStatus = handleMove(boardObject, movePosition)
  handleText(boardObject, buttons)

def createInterface(boardObject):
  rows = boardObject.totalRows
  columns = boardObject.totalColumns
  buttons = np.empty(shape=[rows,columns],dtype="object")

  root = tk.Tk()
  root.title("Broccoli")
  #label = tk.Label(root, text="Broccoli Seeker")
  #label.pack()

  for row in range(0, rows):
    for column in range(0, columns):
      button = tk.Button(root,
                        activebackground="white",
                        bg="lightgray",
                        command= partial(handleClick, boardObject, buttons, [row, column]),
                        disabledforeground="gray",
                        text= "",
                        )
      buttons[row, column] = button
      button.grid(row=row, column=column)
      button = None
  
  root.mainloop()
