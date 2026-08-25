import unittest
import numpy as np

from src.logic.board import Board, board_generator

class TestBoardClass(unittest.TestCase):
  def setUp(self):
    self.rows = 8
    self.columns = 6
    self.board_object = Board(self.rows, self.columns)

  def test_board_size(self):
    expect_size = self.rows * self.columns
    self.assertEqual(expect_size,
                     self.board_object.board_size(),
                     "Incorrect board size")

  def test_flag_tile(self):
    flag_pos = [2, 3]
    previous_flagged_status = self.board_object.tiles_board[flag_pos[0], flag_pos[1]]["flagged"]

    self.board_object.flag_tile(not previous_flagged_status,
                                flag_pos[0],
                                flag_pos[1])

    flagged_tile = self.board_object.tiles_board[flag_pos[0], flag_pos[1]]
    self.assertNotEqual(previous_flagged_status,
                        flagged_tile["flagged"],
                        "Flagged status didn't change")

  def test_change_board(self):
    new_rows = int(self.rows / 2)
    new_columns = self.columns * 2
    new_board = np.ndarray(shape=[new_rows, new_columns], dtype=np.int8)

    self.assertNotEqual(new_board.shape[0],
                        self.board_object.board.shape[0],
                        "Board should have different row amount")
    self.assertNotEqual(new_board.shape[1],
                        self.board_object.board.shape[1],
                        "Board should have different column amount")

    self.board_object.change_board(new_board)

    self.assertEqual(new_board.shape[0],
                     self.board_object.board.shape[0],
                     "Board not same row amount after change")
    self.assertEqual(new_board.shape[1],
                     self.board_object.board.shape[1],
                     "Board not same column amount after change")

  def test_change_tiles_board(self):
    new_rows = int(self.rows / 2)
    new_columns = self.columns * 2
    new_tiles_board = np.ndarray(shape=[new_rows, new_columns], dtype=np.object_)

    self.assertNotEqual(new_tiles_board.shape[0],
                        self.board_object.tiles_board.shape[0],
                        "Tiles board should have different row amount")
    self.assertNotEqual(new_tiles_board.shape[1],
                        self.board_object.tiles_board.shape[1],
                        "Tiles board should have different column amount")

    self.board_object.change_tiles_board(new_tiles_board)

    self.assertEqual(new_tiles_board.shape[0],
                     self.board_object.tiles_board.shape[0],
                     "Tiles board not same row amount after change")
    self.assertEqual(new_tiles_board.shape[1],
                     self.board_object.tiles_board.shape[1],
                     "Tiles board not same column amount after change")

  def test_change_broccoli_amount(self):
    new_broccoli_amount = self.board_object.broccoli_amount + 10
    self.board_object.change_broccoli_amount(new_broccoli_amount)

    self.assertEqual(new_broccoli_amount,
                     self.board_object.broccoli_amount,
                     "Incorrect Broccoli amount after change")

  def test_change_avaliable_spaces_amount(self):
    new_avaiable_spaces = self.board_object.available_space + 40
    self.board_object.change_avaliable_spaces_amount(new_avaiable_spaces)

    self.assertEqual(new_avaiable_spaces,
                     self.board_object.available_space,
                     "Incorrect available spaces amount after change")

  def test_change_null_spaces_amount(self):
    new_null_spaces_amount = self.board_object.null_space_amount + 5
    self.board_object.change_null_spaces_amount(new_null_spaces_amount)

    self.assertEqual(new_null_spaces_amount,
                     self.board_object.null_space_amount,
                     "Incorrect null spaces amount after change")

  def test_add_broccoli_position(self):
    self.assertEqual(0,
                     len(self.board_object.broccoli_positions),
                     "Broccoli positions array should be empty")

    self.board_object.add_broccoli_positions([2,2])

    self.assertEqual(1,
                     len(self.board_object.broccoli_positions),
                     "Broccoli positions array should have 1 element")

    self.board_object.add_broccoli_positions([1,2])
    self.board_object.add_broccoli_positions([2,3])

    self.assertEqual(3,
                     len(self.board_object.broccoli_positions),
                     "Broccoli positions array should have 3 elements")

class TestBoardGeneration(unittest.TestCase):
  def setUp(self):
    self.board_object = board_generator(8, 6, 10)

  def test_board_class(self):
    self.assertIsInstance(self.board_object, Board, "The generated object is not a Board object")

  def test_broccoli_filled_board(self):
    self.assertNotEqual(0, self.board_object.broccoli_amount, "Broccoli amount should not be 0")
    self.assertNotEqual(0, len(self.board_object.broccoli_positions), "Broccoli positions array should have at least 1 element")
