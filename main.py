from src.view.printBoard import printBoardOnConsole
from src.view.mainMenuView import createMainMenuView
from src.logic.board import boardGenerator

# Handles the generation of the Board and redirects to the specific game interface
# Input:
#   gameType: The type of interface used for the game
#     1: Play the game in console
#     2: Play the game in an interface
# Output:
#   Nothing
def selectGameType(gameType):
  if gameType == 1:
    rows = int(input("Enter the rows:"))
    columns = int(input("Enter the columns:"))
    broccoliAmount = int(input("Enter the number of broccolis:"))
    boardObject = boardGenerator(rows, columns, broccoliAmount)
    printBoardOnConsole(boardObject)

  else:
    createMainMenuView()

def main():
  invalidGameType = True
  gameType = -1

  while(invalidGameType):
    print("-------------------")
    print("Select a game type:")
    print("1: console game")
    print("2: interface game")
    print("-------------------")
    gameType = int(input("Enter the game type:"))

    if gameType == 1 or gameType == 2:
      invalidGameType = False
    else:
      print("\nInvalid game type")

  selectGameType(gameType)

main()