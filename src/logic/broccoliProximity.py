def out_of_bounds_validation(current_pos, pos, limit = 0):
  """Validates if the current position is out of bounds.

  Args:
   current_pos (array[int]): The new position that is being evaluated
   pos (array[int]): The previous position
   limit (int): The limit value that the position can have (default 0)
  Returns:
    array[int]: Returns the current_pos if the position is not out of bounds.
      Returns pos argument otherwise
  """
  if limit == 0 and current_pos < limit:
    return pos
  
  if limit != 0 and current_pos >= limit:
    return pos
  
  return current_pos

def check_null_spaces(board, pos, h_increment, v_increment, h_limit=0, v_limit=0):
  """Verifies if there are null spaces on the current position.

  In case of null space, moves the position on a tile farder.
  In horizontal or vertical direction based on increments.
  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    pos (array[int]): The previous position
    h_increment (int): The horizontal increment to select the next position
    v_increment (int): The vertical increment to select the next position
    h_limit (int): The horizontal limit that the row position value can take (default 0)
    v_limit (int): The vertical limit that the column position value can take (default 0)
  Returns:
    array[int]: An array of [newRow, newColumn] position if the position is a nullSpace.
      This [newRow, newColumn] position is a position beyond the null space (if possible).
      If it isn't a nullSpace, return the [row, position] of the next position (position with the increment)
  """
  h_position = out_of_bounds_validation(pos[0] + h_increment, pos[0], h_limit) # h_position: horizontal position
  v_position = out_of_bounds_validation(pos[1] + v_increment, pos[1], v_limit) # v_position: vertical position

  if board[h_position, v_position] == -2:
    new_horizontal_position = out_of_bounds_validation(h_position + h_increment,
                                                       h_position, h_limit)
    new_vertical_position = out_of_bounds_validation(v_position + v_increment,
                                                     v_position, v_limit)

    if board[new_horizontal_position, new_vertical_position] == -2:
      new_horizontal_position = h_position
      new_vertical_position = v_position

    return [new_horizontal_position, new_vertical_position]
  
  return [h_position, v_position]

def broccoli_proximity(board, pos, total_rows, total_columns):
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
  horizontal_start = check_null_spaces(board, pos, -1, 0)[0]
  horizontal_end = check_null_spaces(board, pos, 1, 0, total_rows)[0]
  vertical_start = check_null_spaces(board, pos, 0, -1)[1]
  vertical_end = check_null_spaces(board, pos, 0, 1, 0, total_columns)[1]

  for i in range(horizontal_start, horizontal_end + 1):
    for j in range(vertical_start, vertical_end + 1):
      if board[i,j] < 0:
        continue

      board[i,j] += 1

  return board