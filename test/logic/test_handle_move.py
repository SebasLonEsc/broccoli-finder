import unittest

from src.logic.board import board_generator
from src.logic.handleMove import (reveal_all_broccolis,
                                  check_game_status,
                                  handle_rainbow_broccoli)
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
      if flowering_broccoli_on_board:
        break
 
      for column in range(board.shape[1]):
        if board[row, column] == GET_BOARD_VALUE["floweringBroccoli"]:
          flowering_broccoli_on_board = True
          break

    flowering_broccoli_on_tiles_board = False
    for row in range(tiles_board.shape[0]):
      if flowering_broccoli_on_tiles_board:
        break
  
      for column in range(tiles_board.shape[1]):
        if tiles_board[row, column]["tileValue"] == GET_BOARD_VALUE["floweringBroccoli"]:
          flowering_broccoli_on_tiles_board = True
          break

    self.assertTrue(flowering_broccoli_on_board,
                    "There should be a flowering broccoli on the board")

    self.assertTrue(flowering_broccoli_on_tiles_board,
                    "There should be a flowering broccoli on the tiles board")

