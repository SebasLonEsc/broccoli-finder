import unittest
import numpy as np

from src.logic.board import board_generator, Board
from src.logic.handleMove import (reveal_all_broccolis,
                                  check_game_status,
                                  handle_rainbow_broccoli,
                                  check_valid_move,
                                  make_move)
from src.logic.constants.boardValues import GET_BOARD_VALUE
from src.logic.constants.gameValues import GET_GAME_STATUS

class TestRevealAllBroccolis(unittest.TestCase):
  def setUp(self):
    self.board_object = board_generator(5,5,4)

  def test_reveal_all_broccolis(self):
    broccoli_positions = self.board_object.broccoli_positions
    expected_broccoli_amount = self.board_object.broccoli_amount
    tiles_board = self.board_object.tiles_board
    not_revealed_broccoli_count = 0

    for pos in broccoli_positions:
      if not tiles_board[pos[0], pos[1]]["checked"]:
        not_revealed_broccoli_count += 1

    self.assertEqual(expected_broccoli_amount,
                     not_revealed_broccoli_count,
                     "No broccoli should be revealed since there are not played moves")

    altered_tiles_board = reveal_all_broccolis(self.board_object.board,
                                               tiles_board,
                                               broccoli_positions)

    revealed_broccoli_count = 0

    for row in range(altered_tiles_board.shape[0]):
      for column in range(altered_tiles_board.shape[1]):
        if (altered_tiles_board[row, column]["checked"] and
            (altered_tiles_board[row, column]["tileValue"] == GET_BOARD_VALUE["broccoli"] or
             altered_tiles_board[row, column]["tileValue"] == GET_BOARD_VALUE["rainbowBroccoli"])):
          revealed_broccoli_count += 1

    self.assertEqual(expected_broccoli_amount,
                     revealed_broccoli_count,
                     "All broccoli should be revealed")

class TestCheckGameStatus(unittest.TestCase):
  def setUp(self):
    self.board_object = board_generator(4,4,3)

    tiles_board = self.board_object.tiles_board
    broccoli_count = 0
    for pos in self.board_object.broccoli_positions:
      if broccoli_count == 2:
        break

      if broccoli_count == 0:
        tiles_board[pos[0], pos[1]]["checked"] = True
        tiles_board[pos[0], pos[1]]["tileValue"] = GET_BOARD_VALUE["rainbowBroccoli"]
        broccoli_count += 1

      if broccoli_count == 1:
        tiles_board[pos[0], pos[1]]["checked"] = True
        tiles_board[pos[0], pos[1]]["tileValue"] = GET_BOARD_VALUE["floweringBroccoli"]
        broccoli_count += 1

    self.board_object.change_tiles_board(tiles_board)

  def test_game_over(self):
    broccoli_position = self.board_object.broccoli_positions[0]
    game_status = check_game_status(self.board_object.board,
                                    self.board_object.tiles_board,
                                    broccoli_position,
                                    self.board_object.broccoli_amount)

    self.assertEqual(game_status,
                     GET_GAME_STATUS["Game Over"],
                     "The game status should be Game Over")

  def test_keep_playing(self):
    tiles_board = self.board_object.tiles_board
    board = self.board_object.board
    move_position = [0,0]
    found_position = False

    for row in range(tiles_board.shape[0]):
      if found_position:
        break

      for column in range(tiles_board.shape[1]):
        if board[row, column] != GET_BOARD_VALUE["broccoli"]:
          tiles_board[row, column]["checked"] = True
          tiles_board[row, column]["tileValue"] = board[row, column]
          move_position = [row, column]
          found_position = True
          break

    self.board_object.change_tiles_board(tiles_board)

    game_status = check_game_status(self.board_object.board,
                                    self.board_object.tiles_board,
                                    move_position,
                                    self.board_object.broccoli_amount)
    
    self.assertEqual(game_status,
                     GET_GAME_STATUS["Play"],
                     "The game status should be Play")

  def test_win_status(self):
    tiles_board = self.board_object.tiles_board
    board = self.board_object.board
    move_position = [0,0]

    for row in range(tiles_board.shape[0]):      
      for column in range(tiles_board.shape[1]):
        if board[row, column] != GET_BOARD_VALUE["broccoli"]:
          tiles_board[row, column]["checked"] = True
          tiles_board[row, column]["tileValue"] = board[row, column]
          move_position = [row, column]

    self.board_object.change_tiles_board(tiles_board)

    game_status = check_game_status(self.board_object.board,
                                    self.board_object.tiles_board,
                                    move_position,
                                    self.board_object.broccoli_amount)
    
    self.assertEqual(game_status,
                     GET_GAME_STATUS["Win"],
                     "The game status should be Win")

class TestHandleRainbowBroccoli(unittest.TestCase):
  def setUp(self):
    self.board_object = board_generator(4,4,3)

    tiles_board = self.board_object.tiles_board
    board = self.board_object.board
    broccoli_count = 0
    for pos in self.board_object.broccoli_positions:
      if broccoli_count == 1:
        break

      if broccoli_count == 0:
        tiles_board[pos[0], pos[1]]["checked"] = True
        tiles_board[pos[0], pos[1]]["tileValue"] = GET_BOARD_VALUE["rainbowBroccoli"]
        board[pos[0], pos[1]] = GET_BOARD_VALUE["rainbowBroccoli"]
        broccoli_count += 1

    self.board_object.change_tiles_board(tiles_board)
    self.board_object.change_board(board)

  def test_handle_rainbow_broccoli(self):
    total_tiles = self.board_object.board_size()
    board = self.board_object.board
    non_flowering_broccoli_count = 0

    for row in range(board.shape[0]):      
      for column in range(board.shape[1]):
        if board[row, column] != GET_BOARD_VALUE["floweringBroccoli"]:
          non_flowering_broccoli_count += 1

    self.assertEqual(total_tiles,
                     non_flowering_broccoli_count,
                     "There should be zero flowering broccolis on the board")

    tiles_board, board = handle_rainbow_broccoli(board,
                                                 self.board_object.tiles_board,
                                                 self.board_object.broccoli_positions)

    flowering_broccoli_on_board = False
    for row in range(board.shape[0]): 
      for column in range(board.shape[1]):
        if board[row, column] == GET_BOARD_VALUE["floweringBroccoli"]:
          flowering_broccoli_on_board = True
          break

    flowering_broccoli_on_tiles_board = False
    for row in range(tiles_board.shape[0]):  
      for column in range(tiles_board.shape[1]):
        if tiles_board[row, column]["tileValue"] == GET_BOARD_VALUE["floweringBroccoli"]:
          flowering_broccoli_on_tiles_board = True
          break

    self.assertTrue(flowering_broccoli_on_board,
                    "There should be a flowering broccoli on the board")

    self.assertTrue(flowering_broccoli_on_tiles_board,
                    "There should be a flowering broccoli on the tiles board")

class TestCheckValidMove(unittest.TestCase):
  def setUp(self):
    self.board_object = Board(2,2)
    self.null_space_tile_pos = [0,0]
    self.flagged_tile_pos = [0,1]
    self.checked_tile_pos = [1,0]
    self.valid_tile_pos = [1,1]

    null_space = GET_BOARD_VALUE["nullSpace"]
    blank_space = GET_BOARD_VALUE["blankSpace"]
    broccoli = GET_BOARD_VALUE["broccoli"]
    new_board = [[null_space, broccoli],
                 [blank_space, blank_space]]
    self.board_object.change_board(np.array(new_board))

    tiles_board = self.board_object.tiles_board
    tiles_board[self.flagged_tile_pos[0], self.flagged_tile_pos[1]]["flagged"] = True
    tiles_board[self.checked_tile_pos[0], self.checked_tile_pos[1]]["checked"] = True
    self.board_object.change_tiles_board(tiles_board)

  def test_invalid_move(self):
    total_rows = self.board_object.total_rows
    total_columns = self.board_object.total_columns

    low_row_move = [-1, 0]
    low_column_move = [0, -1]
    high_row_move = [total_rows, 0]
    high_column_move = [0, total_columns]

    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  low_row_move,
                                  total_rows,
                                  total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid for row coordinates below 0")

    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  low_column_move,
                                  total_rows,
                                  total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid for column coordinates below 0")

    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  high_row_move,
                                  total_rows,
                                  total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid for row coordinates higher than total rows")

    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  high_column_move,
                                  total_rows,
                                  total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid for column coordinates higher than total column")

  def test_null_space_move(self):
    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  self.null_space_tile_pos,
                                  self.board_object.total_rows,
                                  self.board_object.total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid on null space tiles")

  def test_checked_tile_move(self):
    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  self.checked_tile_pos,
                                  self.board_object.total_rows,
                                  self.board_object.total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid on checked tiles")

  def test_flagged_tile_move(self):
    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  self.flagged_tile_pos,
                                  self.board_object.total_rows,
                                  self.board_object.total_columns)
    self.assertFalse(valid_move,
                     "Move should be invalid on flagged tiles")

  def test_valid_move(self):
    valid_move = check_valid_move(self.board_object.board,
                                  self.board_object.tiles_board,
                                  self.valid_tile_pos,
                                  self.board_object.total_rows,
                                  self.board_object.total_columns)
    self.assertTrue(valid_move,
                    "Move should be valid")

class TestMakeMove(unittest.TestCase):
  def setUp(self):
    self.board_object = Board(3,3)
    self.null_space_tile_pos = [0,0]
    self.valid_tile_pos = [1,1]
    self.broccoli_pos = [0,1]
    self.rainbow_broccoli_pos = [2,2]
    self.proximity_number_pos = [1,2]

    null_space = GET_BOARD_VALUE["nullSpace"]
    blank_space = GET_BOARD_VALUE["blankSpace"]
    broccoli = GET_BOARD_VALUE["broccoli"]
    rainbow_broccoli = GET_BOARD_VALUE["rainbowBroccoli"]
    self.proximity_number = 1
    new_board = [[null_space, broccoli, blank_space],
                 [blank_space, blank_space, self.proximity_number],
                 [blank_space, self.proximity_number, rainbow_broccoli]]
    self.board_object.change_board(np.array(new_board))

    self.board_object.add_broccoli_positions(self.rainbow_broccoli_pos)
    self.board_object.add_broccoli_positions(self.broccoli_pos)

  def test_make_invalid_move(self):
    tiles_board = self.board_object.tiles_board
    move_pos = self.null_space_tile_pos
    new_tiles_board, _ = make_move(self.board_object.board,
                                   self.board_object.tiles_board,
                                   move_pos,
                                   self.board_object.total_rows,
                                   self.board_object.total_columns,
                                   self.board_object.broccoli_positions)

    # Both should be false since board was custom made
    tiles_comparison = tiles_board[move_pos[0], move_pos[1]]["checked"] == new_tiles_board[move_pos[0], move_pos[1]]["checked"]

    self.assertTrue(tiles_comparison,
                    "Both tiles board must be the same due to move being invalid")

  def test_make_move_on_broccoli(self):
    move_pos = self.broccoli_pos
    new_tiles_board, _ = make_move(self.board_object.board,
                                   self.board_object.tiles_board,
                                   move_pos,
                                   self.board_object.total_rows,
                                   self.board_object.total_columns,
                                   self.board_object.broccoli_positions)

    self.assertTrue(new_tiles_board[move_pos[0], move_pos[1]]["checked"],
                    "The tile should be checked after move")

    is_broccoli = new_tiles_board[move_pos[0], move_pos[1]]["tileValue"] == GET_BOARD_VALUE["broccoli"]
    self.assertTrue(is_broccoli,
                    "The tile should be a broccoli")

  def test_make_move_on_proximity_number(self):
    move_pos = self.proximity_number_pos
    new_tiles_board, _ = make_move(self.board_object.board,
                                   self.board_object.tiles_board,
                                   move_pos,
                                   self.board_object.total_rows,
                                   self.board_object.total_columns,
                                   self.board_object.broccoli_positions)

    self.assertTrue(new_tiles_board[move_pos[0], move_pos[1]]["checked"],
                    "The tile should be checked after move")

    is_proximity_number = new_tiles_board[move_pos[0], move_pos[1]]["tileValue"] == self.proximity_number
    self.assertTrue(is_proximity_number,
                    "The tile should be a proximity number " + str(self.proximity_number))

  def test_make_move_on_raibow_broccoli(self):
    move_pos = self.rainbow_broccoli_pos
    new_tiles_board, new_board = make_move(self.board_object.board,
                                    self.board_object.tiles_board,
                                    move_pos,
                                    self.board_object.total_rows,
                                    self.board_object.total_columns,
                                    self.board_object.broccoli_positions)

    self.assertTrue(new_tiles_board[move_pos[0], move_pos[1]]["checked"],
                    "The tile should be checked after move")

    is_rainbow_broccoli = new_tiles_board[move_pos[0], move_pos[1]]["tileValue"] == GET_BOARD_VALUE["rainbowBroccoli"]
    self.assertTrue(is_rainbow_broccoli,
                    "The tile should be a rainbow broccoli")

    flowering_broccoli_on_tiles_board = False
    for row in range(new_tiles_board.shape[0]):
      for column in range(new_tiles_board.shape[1]):
        if new_tiles_board[row, column]["tileValue"] == GET_BOARD_VALUE["floweringBroccoli"]:
          flowering_broccoli_on_tiles_board = True

    flowering_broccoli_on_board = False
    for row in range(new_board.shape[0]):
      for column in range(new_board.shape[1]):
        if new_board[row, column] == GET_BOARD_VALUE["floweringBroccoli"]:
          flowering_broccoli_on_board = True

    self.assertTrue(flowering_broccoli_on_tiles_board,
                    "There should be a flowering broccoli on the tiles board")

    self.assertTrue(flowering_broccoli_on_board,
                    "There should be a flowering broccoli on the board")