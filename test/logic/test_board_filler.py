import random
import unittest
from unittest.mock import patch, Mock

from src.logic.boardFiller import (validate_rainbow_broccoli_chance)
from src.logic.constants.gameValues import (RAINBOW_BROCCOLI_PROPORTION_CHANCES,
                                            RAINBOW_BROCCOLI_CHANCE,
                                            MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI
                                            )

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