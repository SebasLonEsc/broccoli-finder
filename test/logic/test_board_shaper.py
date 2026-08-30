import unittest
import math
from copy import copy

from src.logic.board import Board
from src.logic.boardShaper import (shapes_weight_definer,
                                   define_corner_sizes,
                                   cut_corners_shaper,
                                   cross_shaper,
                                   board_shaper)
from src.logic.constants.boardValues import BOARD_SHAPES, CORNER_GUIDE, GET_BOARD_VALUE

class TestBoardShaperWeightDefiner(unittest.TestCase):
  def setUp(self):
    self.rows = 8
    self.columns = 6
    self.board_object = Board(self.rows, self.columns)
    self.small_row_board_object = Board(2, self.columns)
    self.small_column_board_object = Board(self.rows, 2)
    self.small_size_board_object = Board(3, 3)

  def test_shapes_weight_definer_normal_board(self):
    shapes_weights = shapes_weight_definer(self.board_object)

    self.assertEqual(len(shapes_weights),
                     len(BOARD_SHAPES),
                     "Weights array should be of size "+ str(len(BOARD_SHAPES)))

  def test_shapes_weight_definer_small_row_board(self):
    shapes_weights = shapes_weight_definer(self.small_row_board_object)

    for i in range(len(BOARD_SHAPES)):
      shape = BOARD_SHAPES[i]
      expected_weight = 0

      if shape == "cutCorners" or shape == "randomCutcorners":
        self.assertEqual(expected_weight,
                         shapes_weights[i],
                         "Weight for two-row boards on any cutCorners shape should be " + str(expected_weight))

      if shape == "cross":
        self.assertEqual(expected_weight,
                         shapes_weights[i],
                         "Weight for two-row boards on cross shape should be " + str(expected_weight))

  def test_shapes_weight_definer_small_column_board(self):
    shapes_weights = shapes_weight_definer(self.small_column_board_object)

    for i in range(len(BOARD_SHAPES)):
      shape = BOARD_SHAPES[i]
      expected_weight = 0

      if shape == "cutCorners" or shape == "randomCutcorners":
        self.assertEqual(expected_weight,
                         shapes_weights[i],
                         "Weight for two-column boards on cross shape should be " + str(expected_weight))

      if shape == "cross":
        self.assertEqual(expected_weight,
                         shapes_weights[i],
                         "Weight for two-column boards on cross shape should be " + str(expected_weight))

  def test_shapes_weight_definer_small_size_board(self):
    shapes_weights = shapes_weight_definer(self.small_size_board_object)

    for i in range(len(BOARD_SHAPES)):
      shape = BOARD_SHAPES[i]
      expected_weight = 0

      if shape == "cross":
        self.assertEqual(expected_weight,
                         shapes_weights[i],
                         "Weight for boards smaller than 16 on cross shape should be " + str(expected_weight))

class TestBoardCornerSizeDefiner(unittest.TestCase):
  def setUp(self):
    self.rows = 8
    self.columns = 6
    self.board_object = Board(self.rows, self.columns)
    self.small_row_board_object = Board(2, self.columns)
    self.small_column_board_object = Board(self.rows, 2)

  def test_not_random_corner_sizes(self):
    corner_sizes = define_corner_sizes(self.board_object, False)

    self.assertEqual(4, # For a total of 4 corners
                     corner_sizes.shape[0],
                     "Corner_sizes should have 4 rows in total")
    self.assertEqual(2, # For a total of 2 coordinates of each corners
                     corner_sizes.shape[1],
                     "Corner_sizes should have 2 columns per row")

    corner_size = corner_sizes[0,0]

    for corner in corner_sizes:
      self.assertEqual(corner_size,
                       corner[0],
                       "Corner size should be equal for all corners")

      self.assertEqual(corner_size,
                       corner[1],
                       "Corner size should be equal for all corners")

  def test_random_corner_sizes(self):
    corner_sizes = define_corner_sizes(self.board_object, True)
    horizontal_corner_size_limit = math.floor(self.rows / 2)
    vertical_corner_size_limit = math.floor(self.columns / 2)

    if self.rows % 2 == 0:
      horizontal_corner_size_limit -= 1
  
    if self.columns % 2 == 0:
      vertical_corner_size_limit -= 1

    for corner in corner_sizes:
      row_size = corner[0]
      column_size = corner[1]

      row_valid_size = row_size >= 1 and row_size <= horizontal_corner_size_limit
      column_valid_size = column_size >= 1 and column_size <= vertical_corner_size_limit

      self.assertTrue(row_valid_size, "Row size outside valid range")
      self.assertTrue(column_valid_size, "Column size outside valid range")

  def test_small_row_corner_sizes(self):
    corner_sizes = define_corner_sizes(self.small_row_board_object, False)
    expected_corner_size = 0

    for corner in corner_sizes:
      self.assertEqual(expected_corner_size,
                       corner[0],
                       "Corner size should be 0")

      self.assertEqual(expected_corner_size,
                       corner[1],
                       "Corner size should be 0")

  def test_small_column_corner_sizes(self):
    corner_sizes = define_corner_sizes(self.small_column_board_object, True)
    expected_corner_size = 0

    for corner in corner_sizes:
      self.assertEqual(expected_corner_size,
                       corner[0],
                       "Corner size should be 0")

      self.assertEqual(expected_corner_size,
                       corner[1],
                       "Corner size should be 0")

class TestCutCornersShaper(unittest.TestCase):
  def setUp(self):
    self.rows = 8
    self.columns = 6
    self.board_object = Board(self.rows, self.columns)
    self.not_random_corners_board_object = cut_corners_shaper(copy(self.board_object), False)
    self.random_corners_board_object = cut_corners_shaper(copy(self.board_object), True)

  def test_not_random_cut_corners_board(self):
    shaped_board = self.not_random_corners_board_object.board
    null_spaces_amount = self.not_random_corners_board_object.null_space_amount
    available_space_amount = self.not_random_corners_board_object.available_space
    previous_available_space = self.board_object.available_space

    self.assertNotEqual(0,
                        null_spaces_amount,
                        "Nullspaces amount should not be 0")

    self.assertNotEqual(previous_available_space,
                        available_space_amount,
                        "Available space amount should change upon shaping")

    for corner in CORNER_GUIDE:
      is_null_space = shaped_board[corner[0], corner[1]] == GET_BOARD_VALUE["nullSpace"]

      self.assertTrue(is_null_space)

  def test_not_random_cut_corners_tiles_board(self):
    shaped_tiles_board = self.not_random_corners_board_object.tiles_board

    for corner in CORNER_GUIDE:
      is_null_space = shaped_tiles_board[corner[0], corner[1]]["tileValue"] == GET_BOARD_VALUE["nullSpace"]

      self.assertTrue(is_null_space)

  def test_random_cut_corners_board(self):
    shaped_board = self.random_corners_board_object.board
    null_spaces_amount = self.random_corners_board_object.null_space_amount
    available_space_amount = self.random_corners_board_object.available_space
    previous_available_space = self.board_object.available_space

    self.assertNotEqual(0,
                       null_spaces_amount,
                       "Nullspaces amount should not be 0")

    self.assertNotEqual(previous_available_space,
                        available_space_amount,
                        "Available space amount should change upon shaping")

    for corner in CORNER_GUIDE:
      is_null_space = shaped_board[corner[0], corner[1]] == GET_BOARD_VALUE["nullSpace"]

      self.assertTrue(is_null_space)
  
  def test_random_cut_corners_tiles_board(self):
    shaped_tiles_board = self.random_corners_board_object.tiles_board

    for corner in CORNER_GUIDE:
      is_null_space = shaped_tiles_board[corner[0], corner[1]]["tileValue"] == GET_BOARD_VALUE["nullSpace"]

      self.assertTrue(is_null_space)


class TestCrossShaper(unittest.TestCase):
  def setUp(self):
    self.rows = 8
    self.columns = 6
    self.board_object = Board(self.rows, self.columns)
    self.small_row_board_object = Board(2, self.columns)
    self.small_column_board_object = Board(self.rows, 2)
    self.small_size_board_object = Board(4, 4)

  def test_small_row_board(self):
    not_shaped_board_object = cross_shaper(copy(self.small_row_board_object))
    not_shaped_board = not_shaped_board_object.board
    blank_space_amount = 0
        
    for row in range(not_shaped_board.shape[0]):
      for column in range(not_shaped_board.shape[1]):
        if not_shaped_board[row, column] == GET_BOARD_VALUE["blankSpace"]:
          blank_space_amount += 1

    available_space = self.small_row_board_object.available_space
    self.assertEqual(available_space,
                      blank_space_amount,
                      "Available space amount should be " + str(available_space))

  def test_small_column_board(self):
    not_shaped_board_object = cross_shaper(copy(self.small_column_board_object))
    not_shaped_board = not_shaped_board_object.board
    blank_space_amount = 0
    
    for row in range(not_shaped_board.shape[0]):
      for column in range(not_shaped_board.shape[1]):
        if not_shaped_board[row, column] == GET_BOARD_VALUE["blankSpace"]:
          blank_space_amount += 1

    available_space = self.small_column_board_object.available_space
    self.assertEqual(available_space,
                     blank_space_amount,
                     "Available space amount should be " + str(available_space))

  def test_small_size_board(self):
    not_shaped_board_object = cross_shaper(copy(self.small_size_board_object))
    not_shaped_board = not_shaped_board_object.board
    blank_space_amount = 0

    for row in range(not_shaped_board.shape[0]):
      for column in range(not_shaped_board.shape[1]):
        if not_shaped_board[row, column] == GET_BOARD_VALUE["blankSpace"]:
          blank_space_amount += 1

    available_space = self.small_size_board_object.available_space
    self.assertEqual(available_space,
                     blank_space_amount,
                     "Available space amount should be " + str(available_space))

  def test_cross_shaped_board(self):
    shaped_board_object = cross_shaper(copy(self.board_object))
    shaped_board = shaped_board_object.board
    cross_row = 0
    cross_column = 0
    row_null_space_count = 0
    column_null_space_count = 0

    for row in range(shaped_board.shape[0]):
      if shaped_board[row, 0] == GET_BOARD_VALUE["nullSpace"]:
        cross_row = row
        break

    for column in range(shaped_board.shape[1]):
      if shaped_board[0, column] == GET_BOARD_VALUE["nullSpace"]:
        cross_column = column
        break

    for row in range(shaped_board.shape[0]):
      if shaped_board[row, cross_column] == GET_BOARD_VALUE["nullSpace"]:
        row_null_space_count += 1

    for column in range(shaped_board.shape[1]):
      if shaped_board[cross_row, column] == GET_BOARD_VALUE["nullSpace"]:
        column_null_space_count += 1

    self.assertEqual(row_null_space_count,
                     self.rows,
                     "Total nullSpaces on the cross row should be equal to row size")

    self.assertEqual(column_null_space_count,
                     self.columns,
                     "Total nullSpaces on the cross row should be equal to row size")

    total_null_spaces = row_null_space_count + column_null_space_count - 1
    self.assertEqual(total_null_spaces,
                     shaped_board_object.null_space_amount,
                     "Invalid amount of nullspaces")

    available_spaces_amount = self.board_object.available_space - total_null_spaces
    self.assertEqual(available_spaces_amount,
                     shaped_board_object.available_space,
                     "Invalid amount of available spaces")

  def test_cross_shaped_tiles_board(self):
    shaped_board_object = cross_shaper(copy(self.board_object))
    shaped_tiles_board = shaped_board_object.tiles_board
    cross_row = 0
    cross_column = 0
    row_null_space_count = 0
    column_null_space_count = 0

    for row in range(shaped_tiles_board.shape[0]):
      if shaped_tiles_board[row, 0]["tileValue"] == GET_BOARD_VALUE["nullSpace"]:
        cross_row = row
        break

    for column in range(shaped_tiles_board.shape[1]):
      if shaped_tiles_board[0, column]["tileValue"] == GET_BOARD_VALUE["nullSpace"]:
        cross_column = column
        break

    for row in range(shaped_tiles_board.shape[0]):
      if shaped_tiles_board[row, cross_column]["tileValue"] == GET_BOARD_VALUE["nullSpace"]:
        row_null_space_count += 1

    for column in range(shaped_tiles_board.shape[1]):
      if shaped_tiles_board[cross_row, column]["tileValue"] == GET_BOARD_VALUE["nullSpace"]:
        column_null_space_count += 1

    self.assertEqual(row_null_space_count,
                     self.rows,
                     "Total nullSpaces on the cross row should be equal to row size")

    self.assertEqual(column_null_space_count,
                     self.columns,
                     "Total nullSpaces on the cross row should be equal to row size")

class TestBoardShaper(unittest.TestCase):
  def setUp(self):
    self.rows = 8
    self.columns = 6
    self.board_object = Board(self.rows, self.columns)

  def test_not_shaped_board(self):
    not_shaped_board_object = board_shaper(copy(self.board_object), "square")
    null_space_amount = not_shaped_board_object.null_space_amount
    expected_available_space = self.board_object.available_space

    self.assertEqual(0,
                     null_space_amount,
                     "Nullspace amount should be 0")

    self.assertEqual(expected_available_space,
                     not_shaped_board_object.available_space,
                     "Invalid available space amount")

  def test_cut_corner_shaped_board(self):
    cut_corner_shaped_board_object = board_shaper(copy(self.board_object), "cutCorners")
    null_space_amount = cut_corner_shaped_board_object.null_space_amount
    not_expected_available_space = self.board_object.available_space

    self.assertNotEqual(0,
                     null_space_amount,
                     "Nullspace amount should not be 0")

    self.assertNotEqual(not_expected_available_space,
                     cut_corner_shaped_board_object.available_space,
                     "Invalid available space amount")

  def test_random_cut_corner_shaped_board(self):
    random_cut_corners_shaped_board_object = board_shaper(copy(self.board_object), "randomCutcorners")
    null_space_amount = random_cut_corners_shaped_board_object.null_space_amount
    not_expected_available_space = self.board_object.available_space

    self.assertNotEqual(0,
                        null_space_amount,
                        "Nullspace amount should not be 0")

    self.assertNotEqual(not_expected_available_space,
                        random_cut_corners_shaped_board_object.available_space,
                        "Invalid available space amount")

  def test_cross_shaped_board(self):
    cross_shaped_board_object = board_shaper(copy(self.board_object), "cross")
    null_space_amount = cross_shaped_board_object.null_space_amount
    not_expected_available_space = self.board_object.available_space

    self.assertNotEqual(0,
                        null_space_amount,
                        "Nullspace amount should not be 0")

    self.assertNotEqual(not_expected_available_space,
                        cross_shaped_board_object.available_space,
                        "Invalid available space amount")
    