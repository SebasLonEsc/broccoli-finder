import tkinter as tk
import numpy as np
from functools import partial
from src.logic.handleMove import handleMove
from src.logic.constants.gameValues import *

# Updates the interface when winning or losing the game
# Disables all buttons and reveal all broccolis if is a lost game
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

# Updates the tiles of the board to show the value (empty, proximity number or broccoli) of each affected tile by the player move
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

# Handles the click of the player on a tile of the board
def handleClick(boardObject, buttons, movePosition, winLabel):
  boardObject, gameStatus = handleMove(boardObject, movePosition)
  handleText(boardObject, buttons)

  if gameStatus != 0:
    gameStatusText = WINNINGTEXT

    if gameStatus < 0:
      gameStatusText = LOSINGTEXT

    winLabel.config(text=gameStatusText)
    handleGameStatus(boardObject, buttons, movePosition)

# Creates the interface of the board
def createBoardInterface(boardObject):
  rows = boardObject.totalRows
  columns = boardObject.totalColumns
  buttons = np.empty(shape=[rows,columns],dtype="object")
  tilesBoard = boardObject.tilesBoard

  root = tk.Tk()
  root.title("Broccoli")
  root.grid_columnconfigure(0, weight=1)
  pane = tk.Frame(root)
  pane.grid(row=0, columnspan=columns)

  tk.Label(
    pane,
    text="Broccoli Seeker",
    anchor="center").grid(row=0, columnspan=columns)
  
  lastPane= tk.Frame(root)
  label = tk.Label(lastPane, text="", anchor="center")
  
  for row in range(0, rows):
    pane = tk.Frame(root, bg="lightgray", background="lightgray")
    pane.grid(row=row+1, column=0, columnspan=columns)

    for column in range(0, columns):
      buttonText = ""
      isNullSpace = tilesBoard[row, column]["checked"]
      backgroundColor = "lightgray"

      if isNullSpace:
        buttonText = " "
        backgroundColor = "gray60"

      button = tk.Button(pane,
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
      button.grid(row=0, column=column)
      button = None

  lastPane.grid(row=rows+2, columnspan=columns)
  label.grid(row=0, column=0, columnspan=columns)
  
  root.mainloop()
