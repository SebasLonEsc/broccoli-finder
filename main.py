from src.logic.board import handleBoardGeneration

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

  handleBoardGeneration(gameType)

main()