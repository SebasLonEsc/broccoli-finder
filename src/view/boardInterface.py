import tkinter as tk
from functools import partial
import numpy as np
import math
from src.logic.handleMove import handleMove

def handleText(boardObject, buttons):
  tilesBoard = boardObject.tilesBoard

  for row in range(0, boardObject.totalRows):
    for column in range(0, boardObject.totalColumns):
      buttonText = buttons[row, column].cget("text")

      if buttonText != "":
        continue

      text = tilesBoard[row, column]["tileValue"]

      if text == "0":
        text = " "

      checked = tilesBoard[row, column]["checked"]

      if checked:
        buttons[row, column].config(state=tk.DISABLED)
        buttons[row, column].config(bg="gray70")
        buttons[row, column].config(text=text)

def handleClick(boardObject, buttons, movePosition):
  boardObject, gameStatus = handleMove(boardObject, movePosition)
  handleText(boardObject, buttons)

def createInterface(boardObject):
  rows = boardObject.totalRows
  columns = boardObject.totalColumns
  buttons = np.empty(shape=[rows,columns],dtype="object")
  tilesBoard = boardObject.tilesBoard

  root = tk.Tk()
  root.title("Broccoli")
  label = tk.Label(root, text="Broccoli Seeker", anchor="center")
  label.grid(row=0, column=math.floor(columns/2)-2, columnspan=4)

  for row in range(0, rows):
    for column in range(0, columns):
      buttonText = ""
      isNullSpace = tilesBoard[row, column]["checked"]
      backgroundColor = "lightgray"

      if isNullSpace:
        buttonText = " "
        backgroundColor = "gray60"

      button = tk.Button(root,
                        activebackground="white",
                        anchor="center",
                        bd=1,
                        bg=backgroundColor,
                        command= partial(handleClick, boardObject, buttons, [row, column]),
                        disabledforeground="white",
                        justify="center",
                        height=1,
                        width=3,
                        padx=0,
                        pady=0,
                        text= buttonText,
                        )
      
      if isNullSpace:
        button.config(state=tk.DISABLED)
      buttons[row, column] = button
      button.grid(row=row+1, column=column)
      button = None
  
  root.mainloop()
