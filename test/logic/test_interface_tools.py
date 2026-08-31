import unittest
from pathlib import Path
import tkinter as tk

from src.logic.interfaceTools import (open_pillow_image,
                                      center_window,
                                      close_interface,
                                      go_back)
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

class TestGoBack(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.root_previous_go_back = tk.Tk()
    self.test_number = 0

  def basic_go_back(self, number):
    self.test_number += number

  def complete_go_back(self, number, previous_go_back_func):
    self.test_number += number
    previous_go_back_func()

  def test_basic_go_back_function(self):
    expected_value = 5
    go_back_func = lambda: self.basic_go_back(expected_value)
    go_back(self.root, go_back_func)

    self.assertRaises(tk.TclError, self.root.winfo_name)
    self.assertEqual(expected_value,
                     self.test_number,
                     "The new value after go back function should be " + str(expected_value))

  def test_complete_go_back_function(self):
    number = 5
    expected_value = number + number # Functions sum number and then sum number by number
    self.test_number = 0

    go_back_func = lambda prev_go_back: self.complete_go_back(number, prev_go_back)
    prev_go_back_func = lambda: self.basic_go_back(number)
    go_back(self.root_previous_go_back, go_back_func, prev_go_back_func)

    self.assertRaises(tk.TclError, self.root_previous_go_back.winfo_name)
    self.assertEqual(expected_value,
                     self.test_number,
                     "The new value after go back function should be " + str(expected_value))
