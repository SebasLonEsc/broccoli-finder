import unittest
import tkinter as tk
from unittest.mock import patch

import src.lang.language as Lg
from src.view.newCustomGameMenu import validate_inputs

class TestValidateInputs(unittest.TestCase):
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