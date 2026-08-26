import unittest
import numpy as np

from src.logic.board import Board
from src.logic.broccoliProximity import (out_of_bounds_validation,
                                         check_null_spaces,
                                         broccoli_proximity,
                                         validate_new_coordinate_value,
                                         validate_nullspaces_for_rainbow_broccoli)
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

class TestBroccoliProximity(unittest.TestCase):
  def setUp(self):
    self.board_object = Board(3,3)
    self.cross_board_object = Board(3,3)
    broccoli = GET_BOARD_VALUE["broccoli"]
    null_space = GET_BOARD_VALUE["nullSpace"]
    
    new_board = [[0, 0, 0],
                 [0, broccoli, 0],
                 [0, 0, 0]]
    self.board_object.change_board(np.array(new_board))
    self.broccoli_pos = [1,1]

    new_cross_board = [[0, null_space, 0],
                       [null_space, null_space, null_space],
                       [0, null_space, broccoli]]
    self.cross_board_object.change_board(np.array(new_cross_board))
    self.cross_broccoli_pos = [2,2]

  def test_broccoli_proximity(self):
    filled_board = broccoli_proximity(self.board_object.board,
                                      self.broccoli_pos,
                                      self.board_object.total_rows,
                                      self.board_object.total_columns)
    proximity_numbers_count = 0
    expected_proximity_number_count = 8 # On a 3x3 board with 1 broccoli

    for row in range(filled_board.shape[0]):
      for column in range(filled_board.shape[1]):
        if filled_board[row, column] > 0:
          proximity_numbers_count += 1

    self.assertEqual(proximity_numbers_count,
                     expected_proximity_number_count,
                     "Total count of proximity numbers should be " + str(expected_proximity_number_count))

  def test_broccoli_proximity_cross_board(self):
    filled_board = broccoli_proximity(self.cross_board_object.board,
                                      self.cross_broccoli_pos,
                                      self.cross_board_object.total_rows,
                                      self.cross_board_object.total_columns)
    proximity_numbers_count = 0
    # On a 3x3 cross-shaped board
    # There are only 4 free tiles -1 for the broccoli
    expected_proximity_number_count = 3

    for row in range(filled_board.shape[0]):
      for column in range(filled_board.shape[1]):
        if filled_board[row, column] > 0:
          proximity_numbers_count += 1

    self.assertEqual(proximity_numbers_count,
                     expected_proximity_number_count,
                     "Total count of proximity numbers should be " + str(expected_proximity_number_count))

class TestNewCoordinateValueValidator(unittest.TestCase):
  def test_valid_new_coordinate(self):
    new_coordinate_value = 1
    limit = 0
    comparator = 1
    valid_new_coordinate = validate_new_coordinate_value(new_coordinate_value,
                                                  limit,
                                                  comparator)

    self.assertTrue(valid_new_coordinate, "The new coordinate should be valid")

    new_coordinate_value = 5
    limit = 6
    comparator = -1
    valid_new_coordinate = validate_new_coordinate_value(new_coordinate_value,
                                                         limit,
                                                         comparator)

    self.assertTrue(valid_new_coordinate, "The new coordinate should be valid")

  def test_invalid_new_coordinate(self):
    new_coordinate_value = -1
    limit = 0
    comparator = 1
    valid_new_coordinate = validate_new_coordinate_value(new_coordinate_value,
                                                         limit,
                                                         comparator)

    self.assertFalse(valid_new_coordinate, "The new coordinate should be invalid")

    new_coordinate_value = 7
    limit = 6
    comparator = -1
    valid_new_coordinate = validate_new_coordinate_value(new_coordinate_value,
                                                         limit,
                                                         comparator)

    self.assertFalse(valid_new_coordinate, "The new coordinate should be invalid")

class TestNullSpaceValidatorForRainbowBroccoli(unittest.TestCase):
  def setUp(self):
    self.empty_board_object = Board(3,3)
    self.cornered_board_object = Board(3,3)
    self.cross_board_object = Board(3,3)
    null_space = GET_BOARD_VALUE["nullSpace"]

    cornered_new_board = [[null_space, null_space, null_space],
                         [null_space, 0, null_space],
                         [null_space, null_space, null_space]]
    self.cornered_board_object.change_board(np.array(cornered_new_board))
    self.cornered_valid_pos = [1,1] # Board center

    cross_new_board = [[0, null_space, 0],
                       [null_space, null_space, null_space],
                       [0, null_space, 0]]
    self.cross_board_object.change_board(np.array(cross_new_board))

  def test_null_space_validation_decrement(self):
    board_lower_limit = 0
    increment = -1
    pos = [self.cornered_valid_pos[0]+increment, self.cornered_valid_pos[1]+increment]
    new_pos = validate_nullspaces_for_rainbow_broccoli(self.cornered_board_object.board,
                                                       pos,
                                                       self.cornered_valid_pos,
                                                       increment,
                                                       board_lower_limit,
                                                       board_lower_limit)

    self.assertEqual(new_pos[0],
                     pos[0], # Stops at first pos with increment for the current board
                     "New row coordinate should be " + str(pos[0]))

    self.assertEqual(new_pos[1],
                     pos[1], # Stops at first pos with increment for the current board
                     "New column coordinate should be " + str(pos[1]))

  def test_null_space_validation_increment(self):
    board_lower_limit = self.cornered_board_object.total_rows # Square board, same number of columns
    increment = 1
    pos = [self.cornered_valid_pos[0]+increment, self.cornered_valid_pos[1]+increment]
    new_pos = validate_nullspaces_for_rainbow_broccoli(self.cornered_board_object.board,
                                                        pos,
                                                        self.cornered_valid_pos,
                                                        increment,
                                                        board_lower_limit,
                                                        board_lower_limit)

    self.assertEqual(new_pos[0],
                     pos[0], # Stops at first pos with increment for the current board
                     "New row coordinate should be " + str(pos[0]))

    self.assertEqual(new_pos[1],
                     pos[1], # Stops at first pos with increment for the current board
                     "New column coordinate should be " + str(pos[1]))

  def test_null_space_validation_empty_board(self):
    board_lower_limit = 0
    increment = -1
    current_pos = [2, 2] # Last row and column of a 3x3 board
    pos = [current_pos[0]+increment, current_pos[1]+increment]
    new_pos = validate_nullspaces_for_rainbow_broccoli(self.empty_board_object.board,
                                                        pos,
                                                        current_pos,
                                                        increment,
                                                        board_lower_limit,
                                                        board_lower_limit)

    self.assertEqual(new_pos[0],
                     pos[0], # Stops at first pos with increment for the current board
                     "New row coordinate should be " + str(pos[0]))
    
    self.assertEqual(new_pos[1],
                     pos[1], # Stops at pos due to be a empty tile
                     "New column coordinate should be " + str(pos[1]))

  def test_null_space_validation_cross_board_decrement(self):
    board_lower_limit = 0
    increment = -1
    current_pos = [2, 2] # Last row and column of a 3x3 board
    pos = [current_pos[0]+increment, current_pos[1]+increment]
    new_pos = validate_nullspaces_for_rainbow_broccoli(self.cross_board_object.board,
                                                       pos,
                                                       current_pos,
                                                       increment,
                                                       board_lower_limit,
                                                       board_lower_limit)

    expected_pos = [0,0] # Other side of the cross
    self.assertEqual(new_pos[0],
                     expected_pos[0],
                     "New row coordinate should be " + str(expected_pos[0]))
    
    self.assertEqual(new_pos[1],
                     expected_pos[0],
                     "New column coordinate should be " + str(expected_pos[1]))

  def test_null_space_validation_cross_board_increment(self):
    board_lower_limit = self.cross_board_object.total_rows # Square board, same number of columns
    increment = 1
    current_pos = [0, 0] # First row and column of a 3x3 board
    pos = [current_pos[0]+increment, current_pos[1]+increment]
    new_pos = validate_nullspaces_for_rainbow_broccoli(self.cross_board_object.board,
                                                        pos,
                                                        current_pos,
                                                        increment,
                                                        board_lower_limit,
                                                        board_lower_limit)

    expected_pos = [2,2] # Other side of the cross
    self.assertEqual(new_pos[0],
                     expected_pos[0],
                     "New row coordinate should be " + str(expected_pos[0]))
    
    self.assertEqual(new_pos[1],
                     expected_pos[0],
                     "New column coordinate should be " + str(expected_pos[1]))