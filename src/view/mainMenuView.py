import tkinter as tk
from functools import partial

from src.view.newGameMenu import newGameMenu
from src.logic.interfaceTools import center_window, close_interface, create_info_menu
from src.logic.constants.styleValues import BUTTON_COLOR, BUTTON_ACTIVE_COLOR

def handleNewGame(root):
  """Closes the current window and creates the new game menu window.
  
  Args:
    root (tk.TK): The root windget, the current window that is being displayed
  """
  close_interface(root)
  newGameMenu(create_main_menu_view)

def create_main_menu_view():
  """Creates the main menu window."""
  window_width = 220
  window_height = 80

  root = tk.Tk()
  root.title("Broccolis")
  root.minsize(window_width, window_height)
  root.maxsize(window_width, window_height)
  center_window(root, window_width, window_height)

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  create_info_menu(tk, menu)

  tk.Label(root,
           text="Broccoli Finder",
           anchor="center"
           ).pack(pady=2)
  
  tk.Button(root,
            activebackground=BUTTON_ACTIVE_COLOR,
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(handleNewGame, root),
            justify="center",
            height=1,
            padx=0,
            pady=0,
            text="New Game"
            ).pack(pady=2)
  
  tk.Button(root,
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
            text="Exit",
            ).pack(pady=[4,8])
  
  root.mainloop()