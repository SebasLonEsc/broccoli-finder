import random

#Calculates a valid random position for a broccoli
def defineBroccoliPositions(board, boardObject):
  pos = [0,0]
  invalidPosition = True

  while invalidPosition:
    pos = [random.randrange(0, boardObject["totalRows"]), random.randrange(0, boardObject["totalColumns"])]
    if board[pos[0], pos[1]] == 0:
      invalidPosition = False
  
  return pos

#Fills a board with an specific number of broccolis
def BoardBroccoliFiller(boardObject, broccoliAmount = 1):
  board = boardObject["board"]
  

  if broccoliAmount >= boardObject["availableSpace"]:
    broccoliAmount = boardObject["availableSpace"] - 1

  for i in range(broccoliAmount):
    pos = defineBroccoliPositions(board, boardObject)
    board[pos[0], pos[1]] = -1

  boardObject["board"] = board
  boardObject["broccoliAmount"] = broccoliAmount

  return boardObject