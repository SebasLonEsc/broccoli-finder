from src.logic.handleMove import handleMove
from src.logic.constants.gameValues import *

# Handles the printing of the board on console
def printing(boardObject):
  guideRow = "     "
  separationRow = "   --"
  for j in range(boardObject.tilesBoard.shape[1]):
    complement = "  "
    if j+1 >= 10:
      complement= " "

    guideRow += str(j + 1) + complement
    separationRow += "---"

  print(guideRow)
  print(separationRow)

  for i in range(boardObject.tilesBoard.shape[0]):
    complement = " "

    if i+1 >= 10:
      complement = ""

    row = complement + str(i + 1) + " | "
    for j in range(boardObject.tilesBoard[i].shape[0]):
      row += boardObject.tilesBoard[i,j]["tileValue"] + "  "

    row +="| " +  str(i + 1)
    print(row)

  print(separationRow)
  print(guideRow)

# Prints the board on the console and request the player to make the moves on the game
# Upon losing or wining the game prints the corresponding message
def printBoardOnConsole(boardObject):
  gameStatus = 0
  rowLimit = boardObject.totalRows
  columnLimit = boardObject.totalColumns

  while gameStatus == 0:
    row = int(input("Enter the row:")) - 1
    column = int(input("Enter the column:")) - 1

    if  row < 0 or row >= rowLimit or column < 0 or column >= columnLimit:
      print("Invalid Row or column value")
      continue

    boardObject, gameStatus = handleMove(boardObject, [row, column])
    printing(boardObject)

  if gameStatus == 1:
    print(WINNINGTEXT)
    return 0
  
  if gameStatus == -1:
    print(LOSINGTEXT)
    return 0