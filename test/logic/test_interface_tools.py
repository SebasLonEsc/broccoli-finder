import unittest
from pathlib import Path
import tkinter as tk

from src.logic.interfaceTools import open_pillow_image
from src.logic.constants.imagesPaths import IMAGES_FOLDER, GREEN_BROCCOLI_TILE_IMAGE

class TestOpenPillowImage(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()

  def test_open_pillow_image(self):
    current_dir = Path(__file__).parent.parent # Double .parent to exit the test folder
    image_path = current_dir.parent / "src" / IMAGES_FOLDER / GREEN_BROCCOLI_TILE_IMAGE
    original_image = tk.PhotoImage(file=str(image_path))
    original_width = original_image.width()
    original_height = original_image.height()

    new_width = 10
    new_height = 10
    tk_image = open_pillow_image(image_path, new_height, new_width)

    self.assertNotEqual(tk_image.width(),
                        original_width,
                        "The width should be different from the original image")
    self.assertNotEqual(tk_image.height(),
                        original_height,
                        "The height should be different from the original image")

    self.assertEqual(tk_image.width(),
                     new_width,
                     "The width should change after image opening")
    self.assertEqual(tk_image.height(),
                     new_height,
                     "The height should change after image opening")