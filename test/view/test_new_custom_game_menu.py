import unittest
import math
import tkinter as tk
from unittest.mock import patch

import src.lang.language as Lg
from src.logic.constants.boardValues import BOARD_SIZE_VALUES
from src.logic.constants.gameValues import GAME_BROCCOLI_PERCENTS
from src.view.newCustomGameMenu import validate_inputs, create_new_game

class _MockSpinBox():
  def __init__(self, value):
    self.str_numeric_spin_box = value

  def get(self):
    return self.str_numeric_spin_box
  
class TestValidateInputs(unittest.TestCase):
  def setUp(self):
    self.base_error_message = Lg.lang["InputErrorText"]

  def test_non_numeric_values(self):
    numeric_spin_box = _MockSpinBox("4")
    invalid_numeric_spin_box = _MockSpinBox("4number")

    expected_error_message = Lg.lang["InvalidNumericValue"]
    message = validate_inputs(invalid_numeric_spin_box,
                              numeric_spin_box,
                              numeric_spin_box)
    self.assertEqual(expected_error_message,
                     message,
                     "Error message should be " + expected_error_message)

    message = validate_inputs(numeric_spin_box,
                              invalid_numeric_spin_box,
                              numeric_spin_box)
    self.assertEqual(expected_error_message,
                     message,
                     "Error message should be " + expected_error_message)

    message = validate_inputs(numeric_spin_box,
                              numeric_spin_box,
                              invalid_numeric_spin_box)
    self.assertEqual(expected_error_message,
                     message,
                     "Error message should be " + expected_error_message)

  def test_invalid_row_input(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    board_size_upper_limit = BOARD_SIZE_VALUES["Big"][1]
    numeric_spin_box = _MockSpinBox(str(board_size_lower_limit))
    invalid_lower_limit_spin_box = _MockSpinBox(str(board_size_lower_limit - 1))

    expected_lower_row_value_message = (self.base_error_message
                                        + "\n"
                                        + Lg.lang["InvalidRowLowerLimit"]
                                        + str(board_size_lower_limit))

    message = validate_inputs(invalid_lower_limit_spin_box,
                              numeric_spin_box,
                              numeric_spin_box)
    self.assertEqual(expected_lower_row_value_message,
                     message,
                     "Incorrect lower row limit value error message")

    invalid_upper_limit_spin_box = _MockSpinBox(str(board_size_upper_limit + 1))
    expected_upper_row_value_message = (self.base_error_message
                                        + "\n"
                                        + Lg.lang["InvalidRowUpperLimit"]
                                        + str(board_size_upper_limit))
    
    message = validate_inputs(invalid_upper_limit_spin_box,
                              numeric_spin_box,
                              numeric_spin_box)
    self.assertEqual(expected_upper_row_value_message,
                     message,
                     "Incorrect upper row limit value error message")

  def test_invalid_column_input(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    board_size_upper_limit = BOARD_SIZE_VALUES["Big"][1]
    numeric_spin_box = _MockSpinBox(str(board_size_lower_limit))
    invalid_lower_limit_spin_box = _MockSpinBox(str(board_size_lower_limit - 1))

    expected_lower_column_value_message = (self.base_error_message
                                           + "\n"
                                           + Lg.lang["InvalidColumnLowerLimit"]
                                           + str(board_size_lower_limit))

    message = validate_inputs(numeric_spin_box,
                              invalid_lower_limit_spin_box,
                              numeric_spin_box)
    self.assertEqual(expected_lower_column_value_message,
                     message,
                     "Incorrect lower column limit value error message")

    invalid_upper_limit_spin_box = _MockSpinBox(str(board_size_upper_limit + 1))
    expected_upper_column_value_message = (self.base_error_message
                                           + "\n"
                                           + Lg.lang["InvalidColumnUpperLimit"]
                                           + str(board_size_upper_limit))
    
    message = validate_inputs(numeric_spin_box,
                              invalid_upper_limit_spin_box,
                              numeric_spin_box)
    self.assertEqual(expected_upper_column_value_message,
                     message,
                     "Incorrect upper column limit value error message")

  def test_negative_broccoli_amount(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    numeric_spin_box = _MockSpinBox(str(board_size_lower_limit))
    negative_broccoli_spin_box = _MockSpinBox("-4")

    expected_message = (self.base_error_message
                        + "\n"
                        + Lg.lang["ZeroBroccolisError"])
    
    message = validate_inputs(numeric_spin_box,
                              numeric_spin_box,
                              negative_broccoli_spin_box)

    self.assertEqual(expected_message,
                     message,
                     "Incorrect negative broccoli value error message")

  def test_too_many_broccolis(self):
    board_size_value = 5
    broccoli_percent_limit = GAME_BROCCOLI_PERCENTS["Big"]["Hard"][1]
    broccoli_limit = math.ceil(board_size_value
                               * board_size_value
                               * broccoli_percent_limit)

    numeric_spin_box = _MockSpinBox(board_size_value)
    too_many_broccoli_spin_box = _MockSpinBox(broccoli_limit + 5)

    expected_message = (Lg.lang["BroccoliErrorLimit1"]
                        + str(broccoli_limit)
                        + "\n"
                        + Lg.lang["BroccoliErrorLimit2"])
    message = validate_inputs(numeric_spin_box,
                              numeric_spin_box,
                              too_many_broccoli_spin_box)

    self.assertEqual(expected_message,
                     message,
                     "Incorrect too many broccolis error message")   

  def test_valid_inputs(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    numeric_spin_box = _MockSpinBox(str(board_size_lower_limit))
    broccoli_spin_box = _MockSpinBox("1")

    message = validate_inputs(numeric_spin_box,
                              numeric_spin_box,
                              broccoli_spin_box)

    self.assertEqual(self.base_error_message,
                     message,
                     "Incorrect valid input message")

class TestCreateNewGame(unittest.TestCase):
  def setUp(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]

    self.numeric_spin_box = _MockSpinBox(str(board_size_lower_limit))
    self.mock_go_back_func = lambda: None
    self.base_error_message = Lg.lang["InputErrorText"]
    self.root = tk.Tk()
    self.error_label = tk.Label(self.root)
    self.error_label.pack()

  def test_invalid_inputs(self):
    negative_broccoli_spin_box = _MockSpinBox("-4")
    returned_value = create_new_game(self.root,
                                     self.numeric_spin_box,
                                     self.numeric_spin_box,
                                     negative_broccoli_spin_box,
                                     self.error_label,
                                     self.mock_go_back_func,
                                     self.mock_go_back_func)

    self.assertFalse(returned_value)

    expected_text = (self.base_error_message
                     + "\n"
                     + Lg.lang["ZeroBroccolisError"])
    label_text = self.error_label.cget("text")

    self.assertEqual(expected_text,
                     label_text,
                     "Incorrect error message")

  def test_create_new_game(self):
    with patch("src.view.newCustomGameMenu.create_board_interface") as mocked_board_interface_creation:
      broccoli_spin_box = _MockSpinBox("1")
      create_new_game(self.error_label, # To test destroy widget
                      self.numeric_spin_box,
                      self.numeric_spin_box,
                      broccoli_spin_box,
                      self.error_label,
                      self.mock_go_back_func,
                      self.mock_go_back_func)

      self.assertFalse(self.error_label.winfo_exists(),
                       "Label should have been destroyed")

      mocked_board_interface_creation.assert_called_once()