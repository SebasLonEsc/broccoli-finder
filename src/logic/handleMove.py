def revealAllBroccolis(board, tilesBoard, broccoliAmount):
  """Reveals all of the broccolis of the board when LOSING the game.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tilesBoard (np.ndarray): Matrix containing each tiles of the board
    broccoliAmount (int): The amount of broccolis on the board
  Returns:
    np.ndarray: tilesBoard matrix with the revealed borccolis
  """
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

def checkGameStatus(board, tilesBoard, movePosition, broccoliAmount):
  """Checks the current game status after a move was done.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tilesBoard (np.ndarray): Matrix containing each tiles of the board
    movePosition (array): An array [row, column] of the current move made by the player
    broccoliAmount (int): The amount of broccolis on the board
  Returns:
    int: Returns the current game status
      -1 -> Indicate a lost game.
      0 -> Indicate the game is still on.
      1 -> Indicates a won game
  """
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

def checkValidMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit):
  """Checks if the current move made by the player is a valid one.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tilesBoard (np.ndarray): Matrix containing each tiles of the board
    movePosition (array): An array [row, column] of the current move made by the player
    boardRowLimit (int): The amount of rows on the board
    boardColumnLimit (int): The amount of columns on the board
  Returns:
    bool: True if the move is valid, False otherwise
  """
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

def makeMove(board, tilesBoard, movePosition, boardRowLimit, boardColumnLimit):
  """Makes the move made by the player.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tilesBoard (np.ndarray): Matrix containing each tiles of the board
    movePosition (array): An array [row, column] of the current move made by the player
    boardRowLimit (int): The amount of rows on the board
    boardColumnLimit (int): The amount of columns on the board

  Returns:
    np.array: Updated tileBoard matrix after the player move if valid.
      Returns the unchanged matrix otherwise
  """
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

def handleMove(boardObject, movePosition):
  """Handles the move made by the player.

  Updates the tilesBoard marix if so.
  And validates the game status after the move
  Args:
    boardObject (Board): The object containing all of the information about the board
    movePosition (array): An array [row, column] of the current move made by the player
  Returns:
    Board: Updated boardObject (if the move is valid or a game condition is met)
    int: Status of the game
      -1 -> Indicate a lost game.
      0 -> Indicate the game is still on.
      1 -> Indicates a won game
  """
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