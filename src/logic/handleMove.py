import random

def reveal_all_broccolis(board, tiles_board, broccoli_positions):
  """Reveals all of the broccolis of the board when LOSING the game.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    broccoli_positions (array[array[int,int]]): The positions of the broccolis
  Returns:
    np.ndarray: The tiles board matrix with the revealed borccolis
  """
  for pos in broccoli_positions:
    row = pos[0]
    column = pos[1]
    tiles_board[row, column]["checked"] = True
    tiles_board[row, column]["tileValue"] = board[row, column]
      
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

      if (tiles_board[i,j]["checked"] == True and
          (tiles_board[i,j]["tileValue"] == -3 or
           tiles_board[i,j]["tileValue"] == -4)):
        unchecked_tiles += 1

  if unchecked_tiles != broccoli_amount:
    return 0

  return 1

def handle_rainbow_broccoli(board, tiles_board, broccoli_positions):
  """Reveals 1 broccoli from the board upon revealing a rainbow broccoli

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    broccoli_positions (array[array[int,int]]): The positions of the broccolis
  Returns:
    np.array: Updated tileBoard matrix after the player move if valid.
      Returns the unchanged matrix otherwise
    (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
  """
  invalid_position = True
  pos = []

  if len(broccoli_positions) == 1:
    invalid_position = False
    pos = broccoli_positions[0]

  while invalid_position:
    pos_index = random.randrange(0, len(broccoli_positions))
    pos = broccoli_positions[pos_index]

    if board[pos[0], pos[1]] == -3:
      continue

    invalid_position = False

  tiles_board[pos[0], pos[1]]["checked"] = True
  tiles_board[pos[0], pos[1]]["tileValue"] = -4
  board[pos[0], pos[1]] = -4

  return tiles_board, board

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

def make_move(board, tiles_board, move_position, board_row_limit, board_column_limit, broccoli_positions):
  """Makes the move made by the player.

  Args:
    board (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
    tiles_board (np.ndarray): Matrix containing each tiles of the board
    move_position (array): An array [row, column] of the current move made by the player
    board_row_limit (int): The amount of rows on the board
    board_column_limit (int): The amount of columns on the board
    broccoli_positions (array[array[int,int]]): The positions of the broccolis
  Returns:
    np.array: Updated tileBoard matrix after the player move if valid.
      Returns the unchanged matrix otherwise
    (np.ndarray): The board matrix containg the information about
      nullspaces, broccoli position and proximity
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
    return tiles_board, board

  tiles_board[row, column]["checked"] = True
  tiles_board[row, column]["tileValue"] = board[row, column]

  if board[row, column] == -1:
    return tiles_board, board
  
  if board[row, column] > 0:
    return tiles_board, board

  if board[move_position[0], move_position[1]] == -3:
    return handle_rainbow_broccoli(board, tiles_board, broccoli_positions)    

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

    tiles_board, board = make_move(board,
                                   tiles_board,
                                   new_positions[i],
                                   board_row_limit,
                                   board_column_limit,
                                   broccoli_positions
                                   )

  return tiles_board, board

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
  tiles_board, board = make_move(board,
                                 tiles_board,
                                 move_position,
                                 board_row_limit,
                                 board_column_limit,
                                 board_object.broccoli_positions
                                 )
  board_object.change_tiles_board(tiles_board)
  board_object.change_board(board)

  game_status = check_game_status(board,
                                  tiles_board,
                                  move_position,
                                  broccoli_amount
                                  )

  if game_status < 0: 
    broccoli_positions = board_object.broccoli_positions
    tiles_board = reveal_all_broccolis(board, tiles_board, broccoli_positions)
    board_object.change_tiles_board(tiles_board)
  
  return board_object, game_status