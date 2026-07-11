# Validates if the current position is out of bounds
def outOfBoundsValidation(currentPos, pos, limit = 0):
  if limit == 0 and currentPos < limit:
    return pos
  
  if limit != 0 and currentPos >= limit:
    return pos
  
  return currentPos

# Verifies if there are null spaces on the current position 
# In case of null pases moves the position on tile farder in horizontal or vertical direction based on increments
# hPosition: horizontal position
# vPosition: vertical position
# hIncrement: horizontal increment
# vIncrement: vertical increment
# hLimit: horizontal limit of the board
# vLimit: vertical limit of the board
def checkNullSpaces(board, pos, hIncrement, vIncrement, hLimit = 0, vLimit = 0):
  hPosition = outOfBoundsValidation(pos[0] + hIncrement, pos[0], hLimit)
  vPosition = outOfBoundsValidation(pos[1] + vIncrement, pos[1], vLimit)

  if board[hPosition,vPosition] == -2:
    newHorizontalPosition = outOfBoundsValidation(hPosition + hIncrement, hPosition, hLimit)
    newVerticalPosition = outOfBoundsValidation(vPosition + vIncrement, vPosition, vLimit)

    if board[newHorizontalPosition,newVerticalPosition] == -2:
      newHorizontalPosition = hPosition
      newVerticalPosition = vPosition

    return [newHorizontalPosition, newVerticalPosition]
  
  return [hPosition, vPosition]

# Checks and registers the proximity values of the broccolis on the board matrix
# The numbers indicate how many broccolis are around that specific tile of the board
def broccoliProximity(board, pos, totalRows, totalColumns):
  horizontalStart = checkNullSpaces(board, pos, -1, 0)[0]
  horizontalEnd = checkNullSpaces(board, pos, 1, 0, totalRows)[0]
  verticalStart = checkNullSpaces(board, pos, 0, -1)[1]
  verticalEnd = checkNullSpaces(board, pos, 0, 1, 0, totalColumns)[1]

  for i in range(horizontalStart, horizontalEnd+1):
    for j in range(verticalStart, verticalEnd+1):
      if board[i,j] < 0:
        continue

      board[i,j] += 1

  return board