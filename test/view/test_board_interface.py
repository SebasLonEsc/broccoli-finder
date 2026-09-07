import unittest
import numpy as np
import tkinter as tk
from unittest.mock import patch

from src.logic.constants.boardValues import GET_BOARD_VALUE
from src.logic.board import Board, board_generator
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
    boardInterface.broccoli_counter_value = 1
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

    self.assertEqual(None,
                     return_value,
                     "Returned value should be None")

  def test_handle_flag_tile(self):
    with (patch.object(tk, "PhotoImage") as image,
          patch.object(tk.Button, "config"),
          patch.object(tk.Label, "config")):
      image.return_value = None
      move_position = [0,0]

      expected_counter = boardInterface.broccoli_counter_value - 1
      return_value = boardInterface.handle_flag_tile(self.board_object,
                                                     self.buttons,
                                                     move_position,
                                                     self.broccoli_counter)

      self.assertTrue(return_value, "New flag status should be True")
      self.assertEqual(expected_counter,
                       boardInterface.broccoli_counter_value,
                       "Broccoli counter value should have been reduced by 1")

      expected_counter = boardInterface.broccoli_counter_value + 1
      return_value = boardInterface.handle_flag_tile(self.board_object,
                                                      self.buttons,
                                                      move_position,
                                                      self.broccoli_counter)

      self.assertFalse(return_value, "New flag status should be False")
      self.assertEqual(expected_counter,
                       boardInterface.broccoli_counter_value,
                       "Broccoli counter value should have been increase by 1")

  def tearDown(self):
    self.root.destroy()

class TestHandleRevealBroccolis(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()

    size = 3
    self.board_object = board_generator(size, size, 3)
    self.buttons = np.empty(shape=[size, size], dtype="object")
    self.button_text = "Broccoli"
    for row in range(0, size):
      for column in range(0, size):
        button = tk.Button(self.root, text=self.button_text)
        button.pack()
        self.buttons[row, column] = button

    tiles_board = self.board_object.tiles_board
    rainbow_broccoli_pos = self.board_object.broccoli_positions[1]    
    rainbow_broccoli_tile = tiles_board[rainbow_broccoli_pos[0],
                                        rainbow_broccoli_pos[1]]
    rainbow_broccoli_tile["tileValue"] = GET_BOARD_VALUE["rainbowBroccoli"]

    flowering_broccoli_pos = self.board_object.broccoli_positions[2]
    flowering_broccoli_tile = tiles_board[flowering_broccoli_pos[0],
                                          flowering_broccoli_pos[1]]
    flowering_broccoli_tile["tileValue"] = GET_BOARD_VALUE["floweringBroccoli"]

  def test_handle_reveal_broccolis(self):
    with (patch("src.view.boardInterface.open_pillow_image") as image,
          ):
      image.return_value = None

      move_position = self.board_object.broccoli_positions[0]
      boardInterface.handle_reveal_broccolis(self.board_object,
                                             self.buttons,
                                             move_position)

      broccoli_positions = self.board_object.broccoli_positions
      for pos in broccoli_positions:
        new_text = self.buttons[pos[0], pos[1]].cget("text")
        self.assertNotEqual(self.button_text,
                            new_text,
                            "Button text should have changed")

  def tearDown(self):
    self.root.destroy()