import unittest
import numpy as np
import tkinter as tk
from unittest.mock import patch

from src.logic.board import Board
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

class TestHandleFlagTile(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.broccoli_counter = tk.Label(self.root)
    self.broccoli_counter.pack()

    size = 2
    self.board_object = Board(size, size)
    self.buttons = np.empty(shape=[size, size], dtype="object")
    for row in range(0, size):
      for column in range(0, size):
        button = tk.Button(self.root)
        button.pack()
        self.buttons[row, column] = button

    self.checked_position = [0,1]
    tiles_board = self.board_object.tiles_board
    tile = tiles_board[self.checked_position[0],
                       self.checked_position[1]]
    tile["checked"] = True
    tiles_board[self.checked_position[0],
                self.checked_position[1]] = tile
    self.board_object.change_tiles_board(tiles_board)

  def test_handle_flag_tile_checked(self):
    return_value = boardInterface.handle_flag_tile(self.board_object,
                                                   self.buttons,
                                                   self.checked_position,
                                                   self.broccoli_counter)

    self.assertFalse(return_value, "Returned value should be False")

  def tearDown(self):
    self.root.destroy()