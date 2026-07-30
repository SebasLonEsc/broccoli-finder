def outOfBoundsValidation(currentPos, pos, limit = 0):
  """Validates if the current position is out of bounds.

  Args:
   currentPos (array[int]): The new position that is being evaluated
   pos (array[int]): The previous position
   limit (int): The limit value that the position can have (default 0)
  Returns:
    array[int]: Returns the currentPos if the position is not out of bounds.
      Returns pos argument otherwise
  """
  if limit == 0 and currentPos < limit:
    return pos
  
  if limit != 0 and currentPos >= limit:
    return pos
  
  return currentPos

def checkNullSpaces(board, pos, hIncrement, vIncrement, hLimit=0, vLimit=0):
  """Verifies if there are null spaces on the current position.

  In case of null space, moves the position on a tile farder.
  In horizontal or vertical direction based on increments.
  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    pos (array[int]): The previous position
    hIncrement (int): The horizontal increment to select the next position
    vIncrement (int): The vertical increment to select the next position
    hLimit (int): The horizontal limit that the row position value can take (default 0)
    vLimit (int): The vertical limit that the column position value can take (default 0)
  Returns:
    array[int]: An array of [newRow, newColumn] position if the position is a nullSpace.
      This [newRow, newColumn] position is a position beyond the null space (if possible).
      If it isn't a nullSpace, return the [row, position] of the next position (position with the increment)
  """
  hPosition = outOfBoundsValidation(pos[0] + hIncrement, pos[0], hLimit) # hPosition: horizontal position
  vPosition = outOfBoundsValidation(pos[1] + vIncrement, pos[1], vLimit) # vPosition: vertical position

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

def broccoliProximity(board, pos, total_rows, total_columns):
  """Checks and registers the proximity values of the broccolis on the board matrix.

  The numbers indicate how many broccolis are around that specific tile of the board
  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    pos (array[int]): The previous position
    total_rows (int): The amount of rows on the board
    total_columns (int): The amount of columns on the board
  Returns:
    np.ndarray: The board matrix with the proximity numbers.
      Which indicate the amount of broccolis next to each tile
  """
  horizontalStart = checkNullSpaces(board, pos, -1, 0)[0]
  horizontalEnd = checkNullSpaces(board, pos, 1, 0, total_rows)[0]
  verticalStart = checkNullSpaces(board, pos, 0, -1)[1]
  verticalEnd = checkNullSpaces(board, pos, 0, 1, 0, total_columns)[1]

  for i in range(horizontalStart, horizontalEnd + 1):
    for j in range(verticalStart, verticalEnd + 1):
      if board[i,j] < 0:
        continue

      board[i,j] += 1

  return board