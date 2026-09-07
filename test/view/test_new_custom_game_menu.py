import unittest
import tkinter as tk
from unittest.mock import patch

import src.lang.language as Lg
from src.logic.constants.boardValues import BOARD_SIZE_VALUES
from src.view.newCustomGameMenu import validate_inputs

class TestValidateInputs(unittest.TestCase):
  def setUp(self):
    self.base_error_message = Lg.lang["InputErrorText"]
  class MockSpinBox():
    def __init__(self, value):
      self.str_numeric_value = value

    def get(self):
      return self.str_numeric_value

  def test_non_numeric_values(self):
    numeric_value = self.MockSpinBox("4")
    invalid_numeric_value = self.MockSpinBox("4number")

    expected_error_message = Lg.lang["InvalidNumericValue"]
    message = validate_inputs(invalid_numeric_value,
                              numeric_value,
                              numeric_value)
    self.assertEqual(expected_error_message,
                     message,
                     "Error message should be " + expected_error_message)

    message = validate_inputs(numeric_value,
                              invalid_numeric_value,
                              numeric_value)
    self.assertEqual(expected_error_message,
                     message,
                     "Error message should be " + expected_error_message)

    message = validate_inputs(numeric_value,
                              numeric_value,
                              invalid_numeric_value)
    self.assertEqual(expected_error_message,
                     message,
                     "Error message should be " + expected_error_message)

  def test_invalid_row_input(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    board_size_upper_limit = BOARD_SIZE_VALUES["Big"][1]
    numeric_value = self.MockSpinBox(str(board_size_lower_limit))
    invalid_lower_limit_value = self.MockSpinBox(str(board_size_lower_limit - 1))

    expected_lower_row_value_message = (self.base_error_message
                                        + "\n"
                                        + Lg.lang["InvalidRowLowerLimit"]
                                        + str(board_size_lower_limit))

    message = validate_inputs(invalid_lower_limit_value,
                              numeric_value,
                              numeric_value)
    self.assertEqual(expected_lower_row_value_message,
                     message,
                     "Invalid lower row limit value error message")

    invalid_upper_limit_value = self.MockSpinBox(str(board_size_upper_limit + 1))
    expected_upper_row_value_message = (self.base_error_message
                                        + "\n"
                                        + Lg.lang["InvalidRowUpperLimit"]
                                        + str(board_size_upper_limit))
    
    message = validate_inputs(invalid_upper_limit_value,
                              numeric_value,
                              numeric_value)
    self.assertEqual(expected_upper_row_value_message,
                     message,
                     "Invalid upper row limit value error message")

  def test_invalid_column_input(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    board_size_upper_limit = BOARD_SIZE_VALUES["Big"][1]
    numeric_value = self.MockSpinBox(str(board_size_lower_limit))
    invalid_lower_limit_value = self.MockSpinBox(str(board_size_lower_limit - 1))

    expected_lower_column_value_message = (self.base_error_message
                                           + "\n"
                                           + Lg.lang["InvalidColumnLowerLimit"]
                                           + str(board_size_lower_limit))

    message = validate_inputs(numeric_value,
                              invalid_lower_limit_value,
                              numeric_value)
    self.assertEqual(expected_lower_column_value_message,
                     message,
                     "Invalid lower column limit value error message")

    invalid_upper_limit_value = self.MockSpinBox(str(board_size_upper_limit + 1))
    expected_upper_column_value_message = (self.base_error_message
                                           + "\n"
                                           + Lg.lang["InvalidColumnUpperLimit"]
                                           + str(board_size_upper_limit))
    
    message = validate_inputs(numeric_value,
                              invalid_upper_limit_value,
                              numeric_value)
    self.assertEqual(expected_upper_column_value_message,
                     message,
                     "Invalid upper column limit value error message")

  def test_negative_broccoli_amount(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    numeric_value = self.MockSpinBox(str(board_size_lower_limit))
    negative_broccoli_value = self.MockSpinBox("-4")

    expected_message = (self.base_error_message
                        + "\n"
                        + Lg.lang["ZeroBroccolisError"])
    
    message = validate_inputs(numeric_value,
                              numeric_value,
                              negative_broccoli_value)

    self.assertEqual(expected_message,
                     message,
                     "Invalid negative broccoli value error message")