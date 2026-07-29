# Validates if the current position is out of bounds
# Input:
#   currentPos: the new position that is being evaluated
#   pos: the previous position
#   limit: the limit value that the position can have
# Output:
#   Returns the currentPos if the position is not out of bounds,
#     return pos otherwise
def outOfBoundsValidation(currentPos, pos, limit = 0):
  if limit == 0 and currentPos < limit:
    return pos
  
  if limit != 0 and currentPos >= limit:
    return pos
  
  return currentPos

# Verifies if there are null spaces on the current position 
# In case of null moves the position on a tile farder
#   in horizontal or vertical direction based on increments
# hPosition: horizontal position
# vPosition: vertical position
# hIncrement: horizontal increment
# vIncrement: vertical increment
# hLimit: horizontal limit of the board
# vLimit: vertical limit of the board
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   pos: the current evaluated position
#   hIncrement: the horizontal increment to select the next position
#   vIncrement: the vertical increment to select the next position
#   hLimit(optional): the horizontal limit that the row position value can take
#     default value is 0
#   vLimit(optional): the vertical limit that the column position value can take
#     default value is 0
# Output:
#   Returns an array of [newRow, newColumn] position if the position is a nullSpace
#     this [newRow, newColumn] position is a position beyond the null space (if possible)
#     if is not a nullSpace, return the [row, position] of the next position (position with the increment)
def checkNullSpaces(board, pos, hIncrement, vIncrement, hLimit=0, vLimit=0):
  hPosition = outOfBoundsValidation(pos[0] + hIncrement, pos[0], hLimit)
  vPosition = outOfBoundsValidation(pos[1] + vIncrement, pos[1], vLimit)

  if board[hPosition, vPosition] == -2:
    newHorizontalPosition = outOfBoundsValidation(hPosition + hIncrement,
                                                  hPosition, hLimit)
    newVerticalPosition = outOfBoundsValidation(vPosition + vIncrement,
                                                vPosition, vLimit)

    if board[newHorizontalPosition, newVerticalPosition] == -2:
      newHorizontalPosition = hPosition
      newVerticalPosition = vPosition

    return [newHorizontalPosition, newVerticalPosition]
  
  return [hPosition, vPosition]

# Checks and registers the proximity values of the broccolis on the board matrix
# The numbers indicate how many broccolis are around that specific tile of the board
# Input:
#   board: the board matrix containg the information about
#     nullspaces, broccoli position and proximity
#   pos: the current evaluated position
#   totalRows: the amount of rows on the board
#   totalColumns: the amount of columns on the board
# Output:
#   Returns the board matrix with the proximity numbers
#     that indicate the amount of broccolis next to each tile
def broccoliProximity(board, pos, totalRows, totalColumns):
  horizontalStart = checkNullSpaces(board, pos, -1, 0)[0]
  horizontalEnd = checkNullSpaces(board, pos, 1, 0, totalRows)[0]
  verticalStart = checkNullSpaces(board, pos, 0, -1)[1]
  verticalEnd = checkNullSpaces(board, pos, 0, 1, 0, totalColumns)[1]

  for i in range(horizontalStart, horizontalEnd + 1):
    for j in range(verticalStart, verticalEnd + 1):
      if board[i,j] < 0:
        continue

      board[i,j] += 1

  return board