import tkinter as tk
from functools import partial

import src.lang.language as Lg
from src.lang.eng import english
from src.lang.spa import spanish
from src.view.newGameMenu import new_game_menu
from src.logic.interfaceTools import center_window, close_interface, create_menu
from src.logic.constants.styleValues import BUTTON_COLOR, BUTTON_ACTIVE_COLOR

def change_selected_language(lang_button,
                             game_title_label,
                             new_game_button,
                             exit_button,
                             root):
  """Changes the selected language of the game

  Args:
    lang_button (tk.Label): The language button widget
    game_title_label (tk.Label): The title label widget
    new_game_button (tk.Button): The new game button widget
    exit_button (tk.Button): The exit button widget
    root (tk.Tk): The root windget, the current window that is being displayed
  """
  match Lg.selected_language:
    case "ENG":
      Lg.selected_language = "SPA"
      Lg.lang = spanish
    case "SPA":
      Lg.selected_language = "ENG"
      Lg.lang = english
    case _:
      Lg.selected_language = "ENG"
      Lg.lang = english

  lang_button.config(text=Lg.selected_language)
  game_title_label.config(text=Lg.lang["GameTitle"])
  new_game_button.config(text=Lg.lang["NewGame"])
  exit_button.config(text=Lg.lang["Exit"])
  create_menu(root=root,
              add_game_menu=False,
              add_info_menu=True,
              add_help_menu=True)

def handle_new_game(root):
  """Closes the current window and creates the new game menu window.
  
  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
  """
  close_interface(root)
  new_game_menu(create_main_menu_view)

def create_main_menu_view():
  """Creates the main menu window."""
  window_width = 220
  window_height = 120

  root = tk.Tk()
  root.title("Broccoli Finder")
  root.minsize(window_width, window_height)
  root.maxsize(window_width, window_height)
  center_window(root, window_width, window_height)

  create_menu(root=root,
              add_game_menu=False,
              add_info_menu=True,
              add_help_menu=True)

  lang_frame = tk.Frame(root)
  lang_frame.pack(expand=True, fill="both", padx=4)
  lang_button = tk.Button(lang_frame,
                          activebackground=BUTTON_ACTIVE_COLOR,
                          anchor="center",
                          bd=1,
                          relief="raised",
                          bg=BUTTON_COLOR,
                          justify="center",
                          text=Lg.selected_language,
                          padx=0,
                          pady=0,
                          )
  lang_button.pack(side="right")

  game_title_label = tk.Label(root,
                              text=Lg.lang["GameTitle"],
                              anchor="center"
                              )
  game_title_label.pack()
  
  new_game_button = tk.Button(root,
                              activebackground=BUTTON_ACTIVE_COLOR,
                              anchor="center",
                              bd=1,
                              bg=BUTTON_COLOR,
                              command=partial(handle_new_game, root),
                              justify="center",
                              height=1,
                              padx=0,
                              pady=0,
                              text=Lg.lang["NewGame"]
                              )
  new_game_button.pack(pady=2)
  
  exit_button = tk.Button(root,
                          activebackground=BUTTON_ACTIVE_COLOR,
                          anchor="center",
                          bd=1,
                          bg=BUTTON_COLOR,
                          command= partial(close_interface, root),
                          justify="center",
                          height=1,
                          width=8,
                          padx=0,
                          pady=0,
                          text=Lg.lang["Exit"],
                          )
  exit_button.pack(pady=[4,8])

  lang_button.config(command=partial(change_selected_language,
                                     lang_button,
                                     game_title_label,
                                     new_game_button,
                                     exit_button,
                                     root)
                                     )
  
  root.mainloop()