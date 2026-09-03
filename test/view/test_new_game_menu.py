import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch

import src.lang.language as Lg
from src.logic.constants.boardValues import BOARD_SIZES
from src.view.newGameMenu import open_custom_game_view, create_game

class TestOpenCustomGameView(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.label = tk.Label(self.root)

  def test_handle_new_game(self):
    with patch("src.view.newGameMenu.create_new_game_view"):
      mock_go_back = lambda: None
      open_custom_game_view(self.label, mock_go_back, mock_go_back) # Func closes the widget send as arg

      self.assertFalse(self.label.winfo_exists(),
                       "Label should be destroyed")

  def tearDown(self):
    self.root.destroy()

class TestCreateGameView(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.label = tk.Label(self.root)
    self.game_difficulty = ttk.Combobox(self.root,
                                        values=Lg.lang["GameDifficulties"],
                                        state="readonly")
    self.game_difficulty.pack()
    self.game_difficulty.set(Lg.lang["GameDifficulties"][0])

  def test_handle_new_game(self):
    with patch("src.view.newGameMenu.create_board_interface") as mocked_function:
      mock_go_back = lambda: None
      create_game(self.label,# Func closes the widget send as arg
                  mock_go_back,
                  mock_go_back,
                  self.game_difficulty,
                  BOARD_SIZES[0]
                  )

      self.assertFalse(self.label.winfo_exists(),
                       "Label should be destroyed")

      mocked_function.assert_called_once()

  def tearDown(self):
    self.root.destroy()