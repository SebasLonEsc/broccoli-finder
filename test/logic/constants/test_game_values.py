import unittest
from unittest.mock import patch, Mock

import src.lang.language as Lg
from src.logic.constants.gameValues import get_random_text, get_end_game_text

class TestRandomText(unittest.TestCase):
  def test_single_text_random(self):
    text_array = ["Hello World"]
    returned_text = get_random_text(text_array)

    self.assertEqual(returned_text,
                     text_array[0],
                     "Returned text should be equal to the one in array sample")

  def test_multiple_texts_random(self):
    text_array = ["Hello", "World", "Happy", "Coding"]
    returned_text = get_random_text(text_array)
    valid_text = False

    for text in text_array:
      if text == returned_text:
        valid_text = True
        break

    self.assertTrue(valid_text,
                    "Returned text should be from the array sample")

class TestEndGameText(unittest.TestCase):
  def test_single_end_game_text(self):
    text_array = ["Hello World"]
    mock_dir = {"test_value": text_array}

    with patch.dict(Lg.lang, mock_dir):
      returned_text = get_end_game_text("test_value")

      self.assertEqual(returned_text,
                       text_array[0],
                       "Returned text should be equal to the one in array sample")

  def test_multiple_end_game_text(self):
    text_array = ["Hello", "World", "Happy", "Coding"]
    mock_dir = {"test_value": text_array}

    with patch.dict(Lg.lang, mock_dir):
      returned_text = get_end_game_text("test_value")
      valid_text = False
      
      for text in text_array:
        if text == returned_text:
          valid_text = True
          break
  
      self.assertTrue(valid_text,
                      "Returned text should be from the array sample")