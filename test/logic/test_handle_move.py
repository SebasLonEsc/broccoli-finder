import unittest

from src.logic.board import board_generator
from src.logic.handleMove import reveal_all_broccolis
from src.logic.constants.boardValues import GET_BOARD_VALUE

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