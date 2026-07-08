import tkinter as tk
import numpy as np
import math
from functools import partial
from src.logic.handleMove import handleMove
from src.logic.constants.gameValues import *

def handleGameStatus(boardObject, buttons, movePosition):
  tilesBoard = boardObject.tilesBoard
  for row in range(0, boardObject.totalRows):
    for column in range(0, boardObject.totalColumns):
      checked = tilesBoard[row, column]["checked"]
      isBroccoli = tilesBoard[row, column]["tileValue"] == "-1"
      backgroundColor = "gray70"
      fontColor = "white"

      buttons[row, column].config(state=tk.DISABLED)

      if movePosition[0] == row and movePosition[1] == column:
        backgroundColor = "dark red"
        fontColor = "white"
      else:
        backgroundColor = "gray50"
        fontColor = "dark red"

      if checked and isBroccoli:
        buttons[row, column].config(bg=backgroundColor)
        buttons[row, column].config(disabledforeground=fontColor)
        buttons[row, column].config(text="-1")


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

def handleClick(boardObject, buttons, movePosition, winLabel):
  boardObject, gameStatus = handleMove(boardObject, movePosition)
  handleText(boardObject, buttons)

  if gameStatus != 0:
    gameStatusText = WINNINGTEXT

    if gameStatus < 0:
      gameStatusText = LOSINGTEXT

    winLabel.config(text=gameStatusText)
    handleGameStatus(boardObject, buttons, movePosition)

def createInterface(boardObject):
  rows = boardObject.totalRows
  columns = boardObject.totalColumns
  buttons = np.empty(shape=[rows,columns],dtype="object")
  tilesBoard = boardObject.tilesBoard
  labelColumnPosition = math.floor(columns/2)-2

  if labelColumnPosition < 0:
    labelColumnPosition = 0

  root = tk.Tk()
  root.title("Broccoli")
  tk.Label(
    root,
    text="Broccoli Seeker",
    anchor="center").grid(row=0, column=labelColumnPosition, columnspan=columns)
  
  label = tk.Label(root, text="", anchor="center")
  

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
                        command= partial(handleClick, boardObject, buttons, [row, column], label),
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

  label.grid(row=rows+2, column=labelColumnPosition, columnspan=columns)
  
  root.mainloop()
