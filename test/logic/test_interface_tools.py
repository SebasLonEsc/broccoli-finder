import unittest
from pathlib import Path
import tkinter as tk

from src.logic.interfaceTools import open_pillow_image, center_window, close_interface
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

    new_x_coords = self.root.winfo_x()
    new_y_coords = self.root.winfo_y()

    self.assertEqual(new_x_coords,
                     expected_x_coords,
                     "Screen should be horizontally centered")

    self.assertEqual(new_y_coords,
                     expected_y_coords,
                     "Screen should be vertically centered")

  def tearDown(self):
    self.root.destroy()

class TestCloseInterface(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()

  def test_close_interface(self):
    widget_name = self.root.winfo_name() # tk widget

    self.assertEqual("tk",
                     widget_name,
                     "The widget hasn't been destroyed yet")

    close_interface(self.root)

    self.assertRaises(tk.TclError, self.root.winfo_name)