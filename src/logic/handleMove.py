def checkWinStatus(board, tilesBoard, movePosition, broccoliAmount):
  if board[movePosition[0], movePosition[1]] == -1:
    return -1

  uncheckedTiles = 0  
  for i in range(0, tilesBoard.shape[0]):
    for j in range(0, tilesBoard.shape[1]):
      if movePosition[0] == i and movePosition[1] == j:
        continue

      if tilesBoard[i,j]["checked"] == False:
        uncheckedTiles += 1

  if uncheckedTiles != broccoliAmount:
    return 0

  return 1

def checkMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit):
  positionX = movePosition[0]
  positionY = movePosition[1]

  if positionX < 0 or positionX >= boardRowLimit or positionY < 0 or positionY >= boardColumnLimit:
    return False
  
  if board[positionX, positionY] == -2:
    return False
  
  if tilesBoard[positionX, positionY]["checked"]:
    return False

  return True

def makeMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit):
  validMove = checkMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit)
  positionX = movePosition[0]
  positionY = movePosition[1]

  if not validMove:
    return tilesBoard

  tilesBoard[positionX, positionY]["checked"] = True
  tilesBoard[positionX, positionY]["tileValue"] = str(board[positionX, positionY])

  if board[positionX, positionY] > 0:
    return tilesBoard

  newPositions = [[positionX-1, positionY], [positionX+1, positionY], [positionX, positionY-1], [positionX, positionY+1]]

  for i in range(len(newPositions)):
    validMove = checkMove(board, tilesBoard, newPositions[i], boardRowLimit, boardColumnLimit)

    if not validMove:
      continue

    tilesBoard = makeMove(board, tilesBoard, newPositions[i], boardRowLimit, boardColumnLimit)

  return tilesBoard

def handleMove(boardObject, movePosition):
  board = boardObject.board
  tilesBoard = boardObject.tilesBoard

  if board[movePosition[0], movePosition[1]] == -2:
    return boardObject, 0
  
  boardRowLimit = boardObject.totalRows
  boardColumnLimit = boardObject.totalColumns
  tilesBoard = makeMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit)
  boardObject.ChangeTilesBoard(tilesBoard)

  gameStatus = checkWinStatus(board, tilesBoard, movePosition, boardObject.broccoliAmount)
  
  return boardObject, gameStatus