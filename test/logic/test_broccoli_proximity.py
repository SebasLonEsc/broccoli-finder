import unittest

from src.logic.broccoliProximity import out_of_bounds_validation

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