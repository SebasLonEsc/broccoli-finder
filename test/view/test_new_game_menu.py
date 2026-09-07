import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch
from PIL import Image, ImageTk

import src.lang.language as Lg
from src.logic.constants.boardValues import BOARD_SIZES
from src.view.newGameMenu import (open_custom_game_view,
                                  create_game,
                                  create_board_size_selector_button,
                                  new_game_menu)

class TestOpenCustomGameView(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.label = tk.Label(self.root)

  def test_handle_new_game(self):
    with patch("src.view.newGameMenu.create_custom_game_view"):
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

  def test_create_game(self):
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

class TestCreateBoardSizeSelectorButton(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.label = tk.Label(self.root)
    self.game_difficulty = ttk.Combobox(self.root,
                                        values=Lg.lang["GameDifficulties"],
                                        state="readonly")
    self.game_difficulty.pack()
    self.game_difficulty.set(Lg.lang["GameDifficulties"][0])

  def test_create_board_size_selector_button(self):
    with (patch.object(Image, "open") as pillow_image,
          patch.object(pillow_image, "resize") as mock_resized_image,
          patch.object(ImageTk, "PhotoImage") as mock_photo_image):
      mock_go_back = lambda: None
      mock_resized_image.return_value = ""
      mock_photo_image.return_value = None
      board_size = BOARD_SIZES[0]

      button = create_board_size_selector_button(self.root,
                                                 mock_go_back,
                                                 mock_go_back,
                                                 self.root,
                                                 self.game_difficulty,
                                                 board_size)

      self.assertTrue(button.winfo_exists,
                      "Button should exists")

      button_text = button.cget("text")
      expected_button_text = Lg.lang[board_size]

      self.assertEqual(button_text,
                       expected_button_text,
                       "Button text should be " + expected_button_text)

  def tearDown(self):
    self.root.destroy()

class TestNewGameMenu(unittest.TestCase):
  def test_new_game_manu_creation(self):
    with (patch.object(tk.Tk, "mainloop"),
          patch("src.view.newGameMenu.create_board_size_selector_button")):
      mock_go_back = lambda: None

      root = new_game_menu(mock_go_back)
      self.assertTrue(root.winfo_exists(),
                      "The window should exists")

      title = root.title()
      expected_title = Lg.lang["GameTitle"]
      self.assertEqual(title,
                       expected_title,
                       "Root title should be " + Lg.lang["GameTitle"])

      root.destroy()