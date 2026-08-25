import unittest

from src.logic.constants.gameValues import get_endgame_text

class TestEndGameText(unittest.TestCase):
  def test_single_end_game_text(self):
    text_array = ["Hello World"]
    returned_text = get_endgame_text(text_array)

    self.assertEqual(returned_text,
                     text_array[0],
                     "Returned text should be equal to the one in array sample")

  def test_multiple_end_game_text(self):
    text_array = ["Hello", "World", "Happy", "Coding"]
    returned_text = get_endgame_text(text_array)

    valid_text = False

    for text in text_array:
      if text == returned_text:
        valid_text = True
        break

    self.assertTrue(valid_text,
                    "Returned text should be from the array sample")