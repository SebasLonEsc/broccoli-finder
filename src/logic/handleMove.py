def reveal_all_broccolis(board, tiles_board, broccoli_amount):
  """Reveals all of the broccolis of the board when LOSING the game.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    broccoli_amount (int): The amount of broccolis on the board
  Returns:
    np.ndarray: The tiles board matrix with the revealed borccolis
  """
  counted_broccolis = 0

  for row in range(0, tiles_board.shape[0]):
    for column in range(0, tiles_board.shape[1]):
      if board[row, column] == -1:
        tiles_board[row, column]["checked"] = True
        tiles_board[row, column]["tileValue"] = str(board[row, column])
        counted_broccolis += 1

      if counted_broccolis == broccoli_amount:
        break
  
  return tiles_board

def check_game_status(board, tiles_board, move_position, broccoli_amount):
  """Checks the current game status after a move was done.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    move_position (array): An array [row, column] of the current move made by the player
    broccoli_amount (int): The amount of broccolis on the board
  Returns:
    int: Returns the current game status
      -1 -> Indicate a lost game.
      0 -> Indicate the game is still on.
      1 -> Indicates a won game
  """
  if board[move_position[0], move_position[1]] == -1:
    return -1

  unchecked_tiles = 0  
  for i in range(0, tiles_board.shape[0]):
    for j in range(0, tiles_board.shape[1]):
      if move_position[0] == i and move_position[1] == j:
        continue

      if tiles_board[i,j]["checked"] == False:
        unchecked_tiles += 1

  if unchecked_tiles != broccoli_amount:
    return 0

  return 1

def check_valid_move(board, tiles_board, move_position, board_row_limit, board_column_limit):
  """Checks if the current move made by the player is a valid one.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    move_position (array): An array [row, column] of the current move made by the player
    board_row_limit (int): The amount of rows on the board
    board_column_limit (int): The amount of columns on the board
  Returns:
    bool: True if the move is valid, False otherwise
  """
  row = move_position[0]
  column = move_position[1]

  if (row < 0 or
      row >= board_row_limit or
      column < 0 or
      column >= board_column_limit):
    return False
  
  if board[row, column] == -2:  # Is a nullspace
    return False

  tile_value = tiles_board[row, column]
  if tile_value["checked"] or tile_value["flagged"]: # Already checked or is flagged
    return False

  return True

def make_move(board, tiles_board, move_position, board_row_limit, board_column_limit):
  """Makes the move made by the player.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    move_position (array): An array [row, column] of the current move made by the player
    board_row_limit (int): The amount of rows on the board
    board_column_limit (int): The amount of columns on the board

  Returns:
    np.array: Updated tileBoard matrix after the player move if valid.
      Returns the unchanged matrix otherwise
  """
  valid_move = check_valid_move(board,
                                tiles_board,
                                move_position,
                                board_row_limit,
                                board_column_limit
                                )
  row = move_position[0]
  column = move_position[1]

  if not valid_move:
    return tiles_board

  tiles_board[row, column]["checked"] = True
  tiles_board[row, column]["tileValue"] = str(board[row, column])

  if board[row, column] > 0:
    return tiles_board

  new_positions = [[row - 1, column],
                   [row + 1, column],
                   [row, column - 1],
                   [row, column + 1]
                   ]

  for i in range(len(new_positions)):
    valid_move = check_valid_move(board,
                                  tiles_board,
                                  new_positions[i],
                                  board_row_limit,
                                  board_column_limit
                                  )

    if not valid_move:
      continue

    tiles_board = make_move(board,
                            tiles_board,
                            new_positions[i],
                            board_row_limit,
                            board_column_limit
                            )

  return tiles_board

def handle_move(board_object, move_position):
  """Handles the move made by the player.

  Updates the tiles_board matrix if so.
  And validates the game status after the move
  Args:
    board_object (Board): The object containing all of the information about the board
    move_position (array): An array [row, column] of the current move made by the player
  Returns:
    Board: Updated board object (if the move is valid or a game condition is met)
    int: Status of the game
      -1 -> Indicate a lost game.
      0 -> Indicate the game is still on.
      1 -> Indicates a won game
  """
  board = board_object.board
  tiles_board = board_object.tiles_board
  broccoli_amount = board_object.broccoli_amount

  if board[move_position[0], move_position[1]] == -2:
    return board_object, 0
  
  board_row_limit = board_object.total_rows
  board_column_limit = board_object.total_columns
  tiles_board = make_move(board,
                          tiles_board,
                          move_position,
                          board_row_limit,
                          board_column_limit
                          )
  board_object.change_tiles_board(tiles_board)

  game_status = check_game_status(board,
                                  tiles_board,
                                  move_position,
                                  broccoli_amount
                                  )

  if game_status < 0: 
    tiles_board = reveal_all_broccolis(board, tiles_board, broccoli_amount)
    board_object.change_tiles_board(tiles_board)
  
  return board_object, game_status