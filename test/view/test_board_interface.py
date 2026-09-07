import unittest
import tkinter as tk
from unittest.mock import patch

import src.view.boardInterface as boardInterface

class TestChangeFlagStatus(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.button = tk.Button(self.root)
    self.button.pack()

  def test_change_flag_status(self):
    with (patch.object(tk, "PhotoImage") as image,
          patch.object(tk.Button, "config")):
      image.return_value = None

      expected_flag_status = not boardInterface.flag_command
      boardInterface.change_flag_status(self.button)

      self.assertEqual(expected_flag_status,
                       boardInterface.flag_command,
                       "Incorrect flag status")

  def tearDown(self):
    self.root.destroy()