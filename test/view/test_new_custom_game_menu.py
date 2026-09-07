import unittest
import math

import src.lang.language as Lg
from src.logic.constants.boardValues import BOARD_SIZE_VALUES
from src.logic.constants.gameValues import GAME_BROCCOLI_PERCENTS
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
                     "Incorrect lower row limit value error message")

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
                     "Incorrect upper row limit value error message")

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
                     "Incorrect lower column limit value error message")

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
                     "Incorrect upper column limit value error message")

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
                     "Incorrect negative broccoli value error message")

  def test_too_many_broccolis(self):
    board_size_value = 5
    broccoli_percent_limit = GAME_BROCCOLI_PERCENTS["Big"]["Hard"][1]
    broccoli_limit = math.ceil(board_size_value
                               * board_size_value
                               * broccoli_percent_limit)

    numeric_value = self.MockSpinBox(board_size_value)
    too_many_broccoli_value = self.MockSpinBox(broccoli_limit + 5)

    expected_message = (Lg.lang["BroccoliErrorLimit1"]
                        + str(broccoli_limit)
                        + "\n"
                        + Lg.lang["BroccoliErrorLimit2"])
    message = validate_inputs(numeric_value,
                              numeric_value,
                              too_many_broccoli_value)

    self.assertEqual(expected_message,
                     message,
                     "Incorrect too many broccolis error message")   

  def test_valid_inputs(self):
    board_size_lower_limit = BOARD_SIZE_VALUES["Small"][0]
    numeric_value = self.MockSpinBox(str(board_size_lower_limit))
    broccoli_value = self.MockSpinBox("1")

    message = validate_inputs(numeric_value,
                              numeric_value,
                              broccoli_value)

    self.assertEqual(self.base_error_message,
                     message,
                     "Incorrect valid input message")