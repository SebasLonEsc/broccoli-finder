import unittest
from pathlib import Path
import tkinter as tk

from src.logic.interfaceTools import open_pillow_image, center_window
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

  def tearDown(self):
    self.root.destroy()

class TestCenterWindow(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.root_width = 100
    self.root_height = 50
    root_xy = 0
    root_geometry = (str(self.root_width)
                     + "x"
                     + str(self.root_height)
                     + "+"
                     + str(root_xy)
                     + "+"
                     + str(root_xy))

    self.root.minsize(self.root_width, self.root_height)
    self.root.maxsize(self.root_width, self.root_height)
    self.root.geometry(root_geometry)
    self.root.update()

  def test_center_window(self):
    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()
    expected_x_coords = (screen_width - self.root_width) // 2 # Screen center
    expected_y_coords = (screen_height - self.root_height) // 2 # Screen center

    center_window(self.root, self.root_width, self.root_height)
    self.root.update()

    new_geometry = self.root.geometry()
    separator_position = new_geometry.find("+") # In the geometry, the first + separates size to coordinates
    new_coordinates = new_geometry[separator_position+1:len(new_geometry)].split("+") # Gets the width and height

    self.assertEqual(int(new_coordinates[0]),
                     expected_x_coords,
                     "Screen should be horizontally centered")

    self.assertEqual(int(new_coordinates[1]),
                     expected_y_coords,
                     "Screen should be vertically centered")

  def tearDown(self):
    self.root.destroy()