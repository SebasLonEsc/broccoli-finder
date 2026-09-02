import unittest
import tkinter as tk

import src.lang.language as Lg
from src.view.mainMenuView import change_selected_language

class TestChangeSelectedLanguage(unittest.TestCase):
  def setUp(self):
    self.main_language = Lg.selected_language
    self.root = tk.Tk()
    self.lang_button = tk.Label(self.root, text=Lg.selected_language)
    self.game_title_label = tk.Label(self.root, text=Lg.lang["GameTitle"])
    self.new_game_button = tk.Button(self.root, text=Lg.lang["NewGame"])
    self.exit_button = tk.Button(self.root, text=Lg.lang["Exit"])

    self.lang_button.pack()
    self.game_title_label.pack()
    self.new_game_button.pack()
    self.exit_button.pack()

  def reset_language(self):
    while Lg.selected_language != self.main_language:
      change_selected_language(self.lang_button,
                               self.game_title_label,
                               self.new_game_button,
                               self.exit_button,
                               self.root)

  def test_change_selected_language(self):
    current_language = Lg.selected_language

    change_selected_language(self.lang_button,
                             self.game_title_label,
                             self.new_game_button,
                             self.exit_button,
                             self.root)
    changed_language = Lg.selected_language

    self.assertNotEqual(changed_language,
                        current_language,
                        "Language should've change")

    self.reset_language()