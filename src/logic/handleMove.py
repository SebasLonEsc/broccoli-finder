def validateMove(boardObject, movePosition): #ChECK TO REMOVe
  board = boardObject["board"]

  if board[movePosition] == -2:
    return False

  return True

def checkMove(board, tilesBoard, movePosition):
  if board[movePosition] == -1:
    return -1
  
  for i in range(0, tilesBoard.shape[0]):
    for j in range(0, tilesBoard.shape[1]):
      if movePosition[0] == i and movePosition[1] == j:
        continue

      if tilesBoard[i,j]["checked"] == False:
        return 0

  return 1

def handleMove(boardObject, movePosition):
  board = boardObject["board"]
  tilesBoard = boardObject["tilesBoard"]

  if board[movePosition] == -2:
    return False
  
  gameStatus = checkMove(board, tilesBoard, movePosition)

  if gameStatus == -1:
    return 0 #LOSE THE GAME
  
  if gameStatus == 1:
    return 1 #WIN GAME
  
  
  
  return boardObject