import random
import unittest
from unittest.mock import patch, Mock

from src.logic.board import Board
from src.logic.boardFiller import (validate_rainbow_broccoli_chance,
                                   add_rainbow_broccoli,
                                   define_broccoli_positions)
from src.logic.constants.gameValues import (RAINBOW_BROCCOLI_PROPORTION_CHANCES,
                                            RAINBOW_BROCCOLI_CHANCE,
                                            MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI
                                            )
from src.logic.constants.boardValues import GET_BOARD_VALUE

class TestRainbowBroccoliChanceValidator(unittest.TestCase):
  def test_small_amount_of_broccolis(self):
    small_broccoli_amount = MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI - 1
    broccoli_proportion = 0.25
    add_rainbow_broccoli = validate_rainbow_broccoli_chance(broccoli_proportion, small_broccoli_amount)

    self.assertFalse(add_rainbow_broccoli, "Rainbow broccoli not valid on small amount of broccolis")

  def test_add_rainbow_broccoli_chance(self):
    broccoli_amount = MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI
    broccoli_proportion = RAINBOW_BROCCOLI_PROPORTION_CHANCES[0][0]
    mock_value = int(RAINBOW_BROCCOLI_CHANCE[0] * 100)
    mock_random_int_func = Mock(return_value=mock_value)

    with patch.object(random, "randint", mock_random_int_func):
      add_rainbow_broccoli = validate_rainbow_broccoli_chance(broccoli_proportion, broccoli_amount)
      self.assertTrue(add_rainbow_broccoli, "Rainbow broccoli should be added")

  def test_rainbow_broccoli_no_chance(self):
    broccoli_amount = MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI
    broccoli_proportion = RAINBOW_BROCCOLI_PROPORTION_CHANCES[0][0]
    mock_random_int_func = Mock(return_value=100)

    with patch.object(random, "randint", mock_random_int_func):
      add_rainbow_broccoli = validate_rainbow_broccoli_chance(broccoli_proportion, broccoli_amount)
      self.assertFalse(add_rainbow_broccoli, "Rainbow broccoli should not be added")

  def test_rainbow_broccoli_chance_invalid_proportion(self):
    broccoli_amount = MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI
    broccoli_proportion = 0.01 # 1% of the board is a broccoli
    add_rainbow_broccoli = validate_rainbow_broccoli_chance(broccoli_proportion, broccoli_amount)
    self.assertFalse(add_rainbow_broccoli, "Rainbow broccoli should not be added")

class TestAddRainbowBroccoli(unittest.TestCase):
  def setUp(self):
    self.board_object = Board(8, 6)
    self.broccoli_positions = [[1,1], [0,0]]

  def test_add_rainbow_broccoli(self):
    new_board = add_rainbow_broccoli(self.board_object.board,
                                     self.broccoli_positions,
                                     self.board_object.total_rows,
                                     self.board_object.total_columns)

    board_value = GET_BOARD_VALUE["blankSpace"]
    for pos in self.broccoli_positions:
      if new_board[pos[0], pos[1]] != GET_BOARD_VALUE["blankSpace"]:
        board_value = new_board[pos[0], pos[1]]

    self.assertNotEqual(GET_BOARD_VALUE["blankSpace"],
                        board_value,
                        "The position of the rainbow broccoli should not be a blankspace value")
    
    self.assertEqual(GET_BOARD_VALUE["rainbowBroccoli"],
                     board_value,
                     "Rainbow broccoli not added in board array")

class TestDefineBroccoliPositions(unittest.TestCase):
  def setUp(self):
    self.board_object = Board(8, 6)
    self.small_board_object = Board(2, 2)

    small_board = self.small_board_object.board
    for row in range(small_board.shape[0]):
      for column in range(small_board.shape[1]):
        small_board[row, column] = 4 # Fills the board with a proximity number

    self.small_board_object.change_board(small_board)

  def test_broccoli_position_blank_space(self):
    broccoli_pos = define_broccoli_positions(self.board_object.board, self.board_object)
    row_pos = broccoli_pos[0]
    column_pos = broccoli_pos[1]
    total_rows = self.board_object.total_rows
    total_columns = self.board_object.total_columns

    self.assertTrue(row_pos >= 0, "Broccoli row position can't be negative")
    self.assertTrue(column_pos >= 0, "Broccoli column position can't be negative")
    self.assertTrue(row_pos < total_rows, "Broccoli row position can't be higher than the total amount of rows")
    self.assertTrue(column_pos < total_columns, "Broccoli column position can't be higher than the total amount of columns")

  def test_broccoli_position_proximity_numbers(self):
    broccoli_pos = define_broccoli_positions(self.small_board_object.board, self.small_board_object)
    row_pos = broccoli_pos[0]
    column_pos = broccoli_pos[1]
    total_rows = self.small_board_object.total_rows
    total_columns = self.small_board_object.total_columns

    self.assertTrue(row_pos >= 0, "Broccoli row position can't be negative")
    self.assertTrue(column_pos >= 0, "Broccoli column position can't be negative")
    self.assertTrue(row_pos < total_rows, "Broccoli row position can't be higher than the total amount of rows")
    self.assertTrue(column_pos < total_columns, "Broccoli column position can't be higher than the total amount of columns")