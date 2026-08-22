from src.logic.constants.boardValues import BOARD_VALUES_GUIDE, GET_BOARD_VALUE

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

def check_null_spaces(board, pos, r_increment, c_increment, r_limit=0, c_limit=0):
  """Verifies if there are null spaces on the current position.

  In case of null space, moves the position on a tile farder.
  In row or column direction based on increments.
  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    pos (array[int]): The previous position
    r_increment (int): The row increment to select the next position
    c_increment (int): The column increment to select the next position
    r_limit (int): The row limit that the row position value can take (default 0)
    c_limit (int): The column limit that the column position value can take (default 0)
  Returns:
    array[int]: An array of [newRow, newColumn] position if the position is a nullSpace.
      This [newRow, newColumn] position is a position beyond the null space (if possible).
      If it isn't a nullSpace, return the [row, position] of the next position (position with the increment)
  """
  row = out_of_bounds_validation(pos[0] + r_increment, pos[0], r_limit)
  column = out_of_bounds_validation(pos[1] + c_increment, pos[1], c_limit)
  
  if (board[row, column] in BOARD_VALUES_GUIDE and
      BOARD_VALUES_GUIDE[board[row, column]] == "nullSpace"):
    new_row = out_of_bounds_validation(row + r_increment, row, r_limit)
    new_column = out_of_bounds_validation(column + c_increment, column, c_limit)

    if (board[new_row, new_column] in BOARD_VALUES_GUIDE and
        BOARD_VALUES_GUIDE[board[new_row, new_column]] == "nullSpace"): # Is a corner
      new_row = row
      new_column = column

    return [new_row, new_column]
  
  return [row, column]

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
  staring_row = check_null_spaces(board, pos, -1, 0)[0] # Decrease on row direction
  ending_row = check_null_spaces(board, pos, 1, 0, total_rows)[0] # Increment on row direction
  starting_column = check_null_spaces(board, pos, 0, -1)[1] # Decrease on column direction
  ending_column = check_null_spaces(board, pos, 0, 1, 0, total_columns)[1] # Increment on column direction

  for i in range(staring_row, ending_row + 1):
    for j in range(starting_column, ending_column + 1):
      if board[i,j] < 0:
        continue

      board[i,j] += 1

  return board

def validate_new_position_values(new_pos_value, limit, comparator):
  """Validates if the new pos coordinate is within the board limits

  Args:
    new_pos_value (int): Position coordinate
    limit (int): The limit value that the new_pos_value is within the limits
    compartor (int): Used to validate the row/column limits using the lesser than in both cases
      For limits equal 0 the step is negative so the comparison is done with positive numbers (step * -1)
      For limits bigger than board size the step is positive,
        so the comparison is done with negative numbers (step * -1)
        that way the new pos is lesser than the limit in the comparison
        in that sense, it validates that pos is greater by doing the lesser than operator
  Returns:
    bool: True if the new position is valid, False otherwise
  """
  if new_pos_value*comparator > limit*comparator:
    return True

  return False

def validate_nullspaces_for_rainbow_broccoli(board, pos, previous_pos, step, row_limit, column_limit, continue_signal = True):
  """Validates if the current pos is a nullspace to find

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    step (int): Indicates to increase or decrease the position in case of nullspace
    pos (array[int,int]): The rainbow broccoli position
    row_limit (int): The limit the first value on pos can take
    column_limit (int): The limit the second value on pos can take
    continue_signal (bool): Controls the recursion to only execute the function twice (default True)
      indicates if continue the recursion once in case of a nullspace
  Returns:
    Array [int, int]: The new position to valdiate the ranbow proximity numbers
  """
  null_space_value = GET_BOARD_VALUE["nullSpace"]
  if board[pos[0], pos[1]] != null_space_value:
    return pos

  # Check validate_new_position_values function docstring on comparator arg
  limit_comparator = step * -1

  # Checks if nullspace is in a row direction   
  if (validate_new_position_values(previous_pos[0]+step, row_limit, limit_comparator) and
      board[previous_pos[0]+step, previous_pos[1]] == null_space_value):
    pos = [pos[0]+step, pos[1]]

  # Checks if nullspace is in a column direction
  if (validate_new_position_values(previous_pos[1]+step, column_limit, limit_comparator) and 
      board[previous_pos[0], previous_pos[1]+step] == null_space_value):
    pos = [pos[0], pos[1]+step]

  # Validates if the new row position (after nullspace validation or not) is valid
  if not validate_new_position_values(pos[0], row_limit, limit_comparator):
    pos[0] = row_limit - 1 if row_limit != 0 else 0

  # Validates if the new column position (after nullspace validation or not) is valid
  if not validate_new_position_values(pos[1], column_limit, limit_comparator):
    pos[1] = column_limit - 1 if column_limit != 0 else 0

  # Recalculates a new position one more time if the current position is a nullspace
  if board[pos[0], pos[1]] == null_space_value and continue_signal:
    return validate_nullspaces_for_rainbow_broccoli(board, pos, previous_pos, step, row_limit, column_limit, False)

  return pos

def update_proximity_numbers_for_rainbow_broccoli(board, pos, total_rows, total_columns):
  """Updates the proximity number around rainbow broccoli

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    pos (array[int,int]): The rainbow broccoli position
    total_rows (int): The amount of rows on the board
    total_columns (int): The amount of columns on the board
  Returns:
    np.ndarray: The board matrix with the proximity numbers.
      Which indicate the amount of broccolis next to each tile
  """
  first_pos = [pos[0]-1, pos[1]-1]
  last_pos = [pos[0]+1, pos[1]+1]

  if first_pos[0] < 0:
    first_pos[0] = 0

  if first_pos[1] < 0:
    first_pos[1] = 0

  if last_pos[0] >= total_rows:
    last_pos[0] = total_rows - 1

  if last_pos[1] >= total_columns:
    last_pos[1] = total_columns - 1

  first_pos = validate_nullspaces_for_rainbow_broccoli(board, first_pos, pos, -1, 0, 0)
  last_pos = validate_nullspaces_for_rainbow_broccoli(board, last_pos, pos, 1, total_rows, total_columns)
  
  for row in range(first_pos[0], last_pos[0]+1): # +1 to include last position
    for column in range(first_pos[1], last_pos[1]+1): # +1 to include last position
      if board[row, column] > 0 and board[row, column] <= 8: # Proximity numbers from 1 to 8
        # Proximity numbers for rainbow broccoli starts from 11 to 18
        # 11 being the same as 1 and 18 the same as 8
        board[row, column] += 10 

  return board