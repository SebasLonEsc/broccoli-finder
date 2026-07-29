# Reveals all of the broccolis of the board when LOSING the game
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   tilesBoard: matrix containing each tiles of the board
#   broccoliAmount: the amount of broccolis on the board
# Output:
#   Returns the tilesBoard matrix with the revealed borccolis
def revealAllBroccolis(board, tilesBoard, broccoliAmount):
  countedBroccolis = 0

  for row in range(0, tilesBoard.shape[0]):
    for column in range(0, tilesBoard.shape[1]):
      if board[row, column] == -1:
        tilesBoard[row, column]["checked"] = True
        tilesBoard[row, column]["tileValue"] = str(board[row, column])
        countedBroccolis += 1

      if countedBroccolis == broccoliAmount:
        break
  
  return tilesBoard

# Checks the current game status after a move was done
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   tilesBoard: matrix containing each tiles of the board
#   movePosition: an array [row, column] of the current move made by the player
#   broccoliAmount: the amount of broccolis on the board
# Output:
#   Returns the current game status
#     -1: Indicate a lost game
#      0: Indicate the game is still on
#      1: Indicates a won game
def checkGameStatus(board, tilesBoard, movePosition, broccoliAmount):
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

# Checks if the current move made by the player is a valid one
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   tilesBoard: matrix containing each tiles of the board
#   movePosition: an array [row, column] of the current move made by the player
#   boardRowLimit: the amount of rows on the board
#   boardColumnLimit: the amount of columns on the board
# Output:
#   Returns True if the move is valid, False otherwise
def checkValidMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit):
  positionX = movePosition[0]
  positionY = movePosition[1]

  if (positionX < 0 or
      positionX >= boardRowLimit or
      positionY < 0 or
      positionY >= boardColumnLimit):
    return False
  
  if board[positionX, positionY] == -2:
    return False
  
  if tilesBoard[positionX, positionY]["checked"]:
    return False

  if tilesBoard[positionX, positionY]["flagged"]:
    return False

  return True

# Makes the move made by the player
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   tilesBoard: matrix containing each tiles of the board
#   movePosition: an array [row, column] of the current move made by the player
#   boardRowLimit: the amount of rows on the board
#   boardColumnLimit: the amount of columns on the board
# Output:
#   Returns the tileBoard matrix with the move registered if valid,
#     returns the unchanged matrix otherwise
def makeMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit):
  validMove = checkValidMove(board,
                             tilesBoard,
                             movePosition,
                             boardRowLimit,
                             boardColumnLimit
                             )
  positionX = movePosition[0]
  positionY = movePosition[1]

  if not validMove:
    return tilesBoard

  tilesBoard[positionX, positionY]["checked"] = True
  tilesBoard[positionX, positionY]["tileValue"] = str(board[positionX, positionY])

  if board[positionX, positionY] > 0:
    return tilesBoard

  newPositions = [[positionX - 1, positionY],
                  [positionX + 1, positionY],
                  [positionX, positionY - 1],
                  [positionX, positionY + 1]
                  ]

  for i in range(len(newPositions)):
    validMove = checkValidMove(board,
                               tilesBoard,
                               newPositions[i],
                               boardRowLimit,
                               boardColumnLimit
                               )

    if not validMove:
      continue

    tilesBoard = makeMove(board,
                          tilesBoard,
                          newPositions[i],
                          boardRowLimit,
                          boardColumnLimit
                          )

  return tilesBoard

# Handles the move made by the player. Check if the move if valid,
#   updates the tilesBoard marix if so
#   and validate the game status after the move
# Input:
#   boardObject: the object containing all of the information about the board
#   movePosition: an array [row, column] of the current move made by the player
# Output:
#   Updated boardObject (if the move is valid or a game condition is met)
#   Status of the game
def handleMove(boardObject, movePosition):
  board = boardObject.board
  tilesBoard = boardObject.tilesBoard
  broccoliAmount = boardObject.broccoliAmount

  if board[movePosition[0], movePosition[1]] == -2:
    return boardObject, 0
  
  boardRowLimit = boardObject.totalRows
  boardColumnLimit = boardObject.totalColumns
  tilesBoard = makeMove(board,
                        tilesBoard,
                        movePosition,
                        boardRowLimit,
                        boardColumnLimit
                        )
  boardObject.changeTilesBoard(tilesBoard)

  gameStatus = checkGameStatus(board,
                               tilesBoard,
                               movePosition,
                               broccoliAmount
                               )

  if gameStatus < 0: 
    tilesBoard = revealAllBroccolis(board, tilesBoard, broccoliAmount)
    boardObject.changeTilesBoard(tilesBoard)
  
  return boardObject, gameStatus