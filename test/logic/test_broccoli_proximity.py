import unittest
import numpy as np

from src.logic.board import Board
from src.logic.broccoliProximity import out_of_bounds_validation, check_null_spaces
from src.logic.constants.boardValues import GET_BOARD_VALUE

class TestOutOfBoundsValidation(unittest.TestCase):
  def test_limit_zero_coordinate(self):
    limit = 0
    new_coordinate = -1
    current_coordinate = 0
    validated_coordinate = out_of_bounds_validation(new_coordinate, current_coordinate, limit)

    self.assertEqual(validated_coordinate,
                     current_coordinate,
                     "The expected coordinate should be the current one")

  def test_non_zero_limit_coordinate(self):
    limit = 8
    new_coordinate = 8
    current_coordinate = 7
    validated_coordinate = out_of_bounds_validation(new_coordinate, current_coordinate, limit)

    self.assertEqual(validated_coordinate,
                     current_coordinate,
                     "The expected coordinate should be the current one")

  def test_valid_new_coordinate(self):
    limit = 0
    new_coordinate = 0
    current_coordinate = 1
    validated_coordinate = out_of_bounds_validation(new_coordinate, current_coordinate, limit)

    self.assertEqual(validated_coordinate,
                      new_coordinate,
                      "The expected coordinate should be the new one")

    limit = 8
    new_coordinate = 7
    current_coordinate = 6
    validated_coordinate = out_of_bounds_validation(new_coordinate, current_coordinate, limit)

    self.assertEqual(validated_coordinate,
                     new_coordinate,
                     "The expected coordinate should be the new one")

class TestCheckNullSpaces(unittest.TestCase):
  def setUp(self):
    self.cross_board_object = Board(3,3)
    self.corner_board_object = Board(2,2)
    null_space = GET_BOARD_VALUE["nullSpace"]

    new_cross_board = [[0, null_space, 0],
                       [null_space, null_space, null_space],
                       [0, null_space, 0]]
    self.cross_board_object.change_board(np.array(new_cross_board))

    new_corner_board = [[null_space, null_space],
                        [null_space, 0]]
    self.corner_board_object.change_board(np.array(new_corner_board))
    self.current_corner_pos = [1,1] # Last row last column, 1 nullSpace tile up and outside board beyond

  def test_decrease_pos_value(self):
    current_pos = [2,2]
    increment = -1
    new_pos = check_null_spaces(self.cross_board_object.board,
                                current_pos,
                                increment,
                                increment)
    expected_pos = [0,0] # The pos at the other side of the cross shape

    self.assertEqual(new_pos[0],
                     expected_pos[0],
                     "Invalid row coordinate")

    self.assertEqual(new_pos[1],
                     expected_pos[1],
                     "Invalid column coordinate")

  def test_increase_pos_value(self):
    current_pos = [0,0]
    increment = 1
    new_pos = check_null_spaces(self.cross_board_object.board,
                                current_pos,
                                increment,
                                increment,
                                self.cross_board_object.total_rows,
                                self.cross_board_object.total_columns)
    expected_pos = [2,2] # The pos at the other side of the cross shape

    self.assertEqual(new_pos[0],
                     expected_pos[0],
                     "Invalid row coordinate")

    self.assertEqual(new_pos[1],
                     expected_pos[1],
                     "Invalid column coordinate")

  def test_invalid_pos_increment_value(self):
    current_pos = [0,0]
    increment = -1
    new_pos = check_null_spaces(self.cross_board_object.board,
                                current_pos,
                                increment,
                                increment)

    self.assertEqual(new_pos[0],
                     current_pos[0],
                     "Invalid row coordinate")

    self.assertEqual(new_pos[1],
                     current_pos[1],
                     "Invalid column coordinate")

  def test_invalid_outside_board_increment_value(self):
    increment = -1
    expected_pos = [self.current_corner_pos[0]-1,
                    self.current_corner_pos[1]] # Move -1 in row coordinate
    new_pos = check_null_spaces(self.corner_board_object.board,
                                self.current_corner_pos,
                                increment,
                                0)

    self.assertEqual(new_pos[0],
                     expected_pos[0],
                     "Row coordinate should not change")

    self.assertEqual(new_pos[1],
                     expected_pos[1],
                     "Column coordinate should not change")