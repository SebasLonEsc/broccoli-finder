from PIL import Image, ImageTk
from functools import partial
import tkinter as tk

import src.lang.language as Lg

def open_pillow_image(image_path, width, height):
  """Opens an image with pillow library

  Args:
    image_path (Path): The path of the image
    width (int): The width of the image
    height (int): The height of the image
  Returns:
    PhotoImage: Returns an image in tkinter format
  """
  image = Image.open(image_path)
  image = image.resize((width, height), Image.Resampling.BOX)
  tile_image = ImageTk.PhotoImage(image, size=[width, height])
  return tile_image

def center_window(window, window_width, window_height):
  """Places the window at the center of the screen.

  Args:
    window (tk.widget): The root windget, the current window that is being displayed
    window_width (int): The width of the current window
    window_height (int): The height of the current window
  """
  screen_width = window.winfo_screenwidth()
  screen_height = window.winfo_screenheight()
  x = (screen_width - window_width) // 2 # Screen center
  y = (screen_height - window_height) // 2 # Screen center
  window.geometry("+%d+%d" % (x, y))

def close_interface(root):
  """Closes the current window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
  """
  root.destroy()

def go_back(root, go_back_func, previous_go_back_func=None):
  """Closes the current window and creates the new game menu window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    go_back_func (Func): The current go_back function.
      Used to go back to the previous view
    previous_go_back_func (Func): The go_back function of the previous view.
      Used to go back two views prior (default None)
  """
  close_interface(root)

  if previous_go_back_func is None:
    go_back_func()
  else:
    go_back_func(previous_go_back_func)

def create_top_level(message, title, width, height):
  """Creates a toplevel widget with a message and title.

  Args:
    message (str): The message to be displayed on the toplevel
    title (str): The title of the toplevel
  """
  top_level = tk.Toplevel()
  top_level.title(title)
  top_level.geometry(str(width) + "x" + str(height))

  message_widget = tk.Message(top_level, text=message)
  close_button = tk.Button(top_level,
                           text="Close",
                           command=top_level.destroy
                           )

  message_widget.pack()
  close_button.pack(pady=[2,0])
  top_level.mainloop()

def create_info_menu(menu_widget):
  """Creates the info menu.

  Args:
    menu_widget (tk.Widget): The menu widget where the menu is going to be attached
  """
  info_menu = tk.Menu(menu_widget, tearoff=0)
  menu_widget.add_cascade(label=Lg.lang["InfoTabMenu"], menu=info_menu)

  about_message = "".join(Lg.lang["AboutMessage"])
  info_menu.add_command(label=Lg.lang["AboutMenuLabel"],
                        command=lambda: create_top_level(about_message, Lg.lang["AboutMenuLabel"], 420, 270)
                        )

  credits_message = "".join(Lg.lang["CreditsMessage"])
  info_menu.add_command(label=Lg.lang["CreditsMenuLabel"],
                        command=lambda: create_top_level(credits_message, Lg.lang["CreditsMenuLabel"], 400, 280)
                        )

def create_help_menu(menu_widget):
  """Creates the help menu.
  
  Args:
    menu_widget (tk.Widget): The menu widget where the menu is going to be attached
  """
  help_menu = tk.Menu(menu_widget, tearoff=0)
  menu_widget.add_cascade(label=Lg.lang["HelpTabMenu"], menu=help_menu)

  how_to_play_message = "".join(Lg.lang["HowToPlayMessage"])
  help_menu.add_command(label=Lg.lang["HowToPlayMenuLabel"],
                        command=lambda: create_top_level(how_to_play_message, Lg.lang["HowToPlayMenuLabel"], 620, 440)
                        )

  rainbow_broccoli_message = "".join(Lg.lang["SpecialBroccolisMessage"])
  help_menu.add_command(label=Lg.lang["SpecialBroccolisMenuLabel"],
                        command=lambda: create_top_level(rainbow_broccoli_message, Lg.lang["SpecialBroccolisMenuLabel"], 500, 350)
                        )

def create_menu(root,
                add_game_menu = True,
                add_main_menu_shortcut = False,
                main_menu_shortcut = None,
                add_new_game_shortcut = False,
                new_game_shortcut = None,
                add_info_menu = False,
                add_help_menu = False
                ):
  """Creates the top menu.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    add_game_menu (bool): Indicates if the game menu needs to be added (default: True)
    add_main_menu_shortcut (bool): Indicates if the main menu shortcut needs to be added.
      Requires the add_game_menu to be True (default False)
    main_menu_shortcut (Func): The function to go to the main menu.
      Requires the add_game_menu and add_main_menu_shortcut to be True (default None)
    add_new_game_shortcut (bool): Indicates if the new game shortcut needs to be added.
      Requires the add_game_menu to be True (default False)
    new_game_shortcut (Func): The function to go to the new game screen.
      Requires the add_game_menu and add_new_game_shortcut to be True (default None)
    add_info_menu (bool): Indicates if the info menu needs to be added (default False)
    add_help_menu (bool): Indicates if the help menu needs to be added (default False)
  """
  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)

  if add_game_menu:
    game_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label=Lg.lang["GameTabMenu"], menu=game_menu)

    separator = False
    if(add_new_game_shortcut and
      new_game_shortcut is not None and
      main_menu_shortcut is not None):
      game_menu.add_command(label=Lg.lang["NewGameLabel"], command=partial(go_back, root, new_game_shortcut, main_menu_shortcut))
      separator = True

    if (add_main_menu_shortcut and main_menu_shortcut is not None):
      game_menu.add_command(label=Lg.lang["MainMenuLabel"], command=partial(go_back, root, main_menu_shortcut))
      separator = True

    if separator:
      game_menu.add_separator()

    game_menu.add_command(label=Lg.lang["Exit"], command=partial(close_interface, root))

  if add_info_menu:
    create_info_menu(menu)

  if add_help_menu:
    create_help_menu(menu)