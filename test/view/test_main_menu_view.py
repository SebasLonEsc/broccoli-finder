import unittest
import tkinter as tk
from unittest.mock import patch

import src.lang.language as Lg
from src.lang.language import LANGUAGES
from src.lang.spa import spanish
from src.view.mainMenuView import (change_selected_language,
                                   handle_new_game,
                                   create_main_menu_view)

class TestChangeSelectedLanguage(unittest.TestCase):
  def setUp(self):
    self.main_language = LANGUAGES["English"]
    self.root = tk.Tk()
    self.lang_button = tk.Label(self.root, text=Lg.selected_language)
    self.game_title_label = tk.Label(self.root, text=Lg.lang["GameTitle"])
    self.new_game_button = tk.Button(self.root, text=Lg.lang["NewGame"])
    self.exit_button = tk.Button(self.root, text=Lg.lang["Exit"])

    self.lang_button.pack()
    self.game_title_label.pack()
    self.new_game_button.pack()
    self.exit_button.pack()

  def reset_language(self, expected_language):
    menu = None

    while Lg.selected_language != expected_language:
      menu = change_selected_language(self.lang_button,
                                      self.game_title_label,
                                      self.new_game_button,
                                      self.exit_button,
                                      self.root)

    return menu

  def test_change_selected_language(self):
    change_selected_language(self.lang_button,
                             self.game_title_label,
                             self.new_game_button,
                             self.exit_button,
                             self.root)
    changed_language = Lg.selected_language

    self.assertNotEqual(changed_language,
                        self.main_language,
                        "Language should've change")

    Lg.selected_language = "InvalidLang"
    change_selected_language(self.lang_button,
                             self.game_title_label,
                             self.new_game_button,
                             self.exit_button,
                             self.root)
    
    self.assertEqual(Lg.selected_language,
                     self.main_language,
                     "Language should've change to default one")

  def test_change_language_widgets(self):
    expected_lang_button_label = LANGUAGES["Spanish"]
    expected_game_title_label = spanish["GameTitle"]
    expected_new_game_button_label = spanish["NewGame"]
    expected_exit_button_label = spanish["Exit"]

    self.reset_language(LANGUAGES["Spanish"])

    self.assertEqual(self.lang_button.cget("text"),
                     expected_lang_button_label,
                     "Lang button label should've change")

    self.assertEqual(self.game_title_label.cget("text"),
                     expected_game_title_label,
                     "Game title label should've change")

    self.assertEqual(self.new_game_button.cget("text"),
                     expected_new_game_button_label,
                     "New game button label should've change")

    self.assertEqual(self.exit_button.cget("text"),
                    expected_exit_button_label,
                    "Exit button label should've change")

  def test_change_language_menu(self):
    menu = self.reset_language(LANGUAGES["Spanish"])
    info_menu_label = spanish["InfoTabMenu"]
    info_menu = None
    
    info_menu_name = menu.entrycget(info_menu_label, "menu")
    info_menu = self.root.nametowidget(info_menu_name)

    self.assertNotEqual(info_menu,
                        None,
                        "Info menu should exist on the menu")

    help_menu_label = spanish["HelpTabMenu"]
    help_menu = None
    
    help_menu_name = menu.entrycget(help_menu_label, "menu")
    help_menu = self.root.nametowidget(help_menu_name)

    self.assertNotEqual(help_menu,
                        None,
                        "Help menu should exist on the menu")

  def tearDown(self):
    self.reset_language(self.main_language)
    self.root.destroy()

class TestHandleNewGame(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.label = tk.Label(self.root)

  def test_handle_new_game(self):
    with patch("src.view.mainMenuView.new_game_menu"):
      handle_new_game(self.label) # Func closes the widget send as arg

      self.assertFalse(self.label.winfo_exists(),
                       "Label should be destroyed")

  def tearDown(self):
    self.root.destroy()

class TestCreateMainView(unittest.TestCase):
  def test_create_main_menu_view(self):
    with (patch.object(tk.Tk, "mainloop"),
          patch.object(tk, "PhotoImage") as mock_photo_image,
          patch.object(tk.Tk, "iconphoto")):
      mock_photo_image.return_value = ""

      root = create_main_menu_view()
      title = root.title()
      expected_title = Lg.lang["GameTitle"]

      self.assertEqual(title,
                       expected_title,
                       "Root title should be " + Lg.lang["GameTitle"])

      root.destroy()