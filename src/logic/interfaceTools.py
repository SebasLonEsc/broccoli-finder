from PIL import Image, ImageTk

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
  x = (screen_width - window_width) // 2
  y = (screen_height - window_height) // 2
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

def create_top_level(tk, message, title, width, height):
  """Creates a toplevel widget with a message and title.

  Args:
    tk (tk): The tk library reference.
      Passed as argument to reduce double referencing on this file.
      Just a personal preference for this case
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

def create_info_menu(tk, menu_widget):
  """Creates the info menu.

  Args:
    tk (tk): The tk library reference.
      Passed as argument to reduce double referencing on this file.
      Just a personal preference for this case
    menu_widget (tk.Widget): The menu widget where the menu is going to be attached
  """
  info_menu = tk.Menu(menu_widget, tearoff=0)
  menu_widget.add_cascade(label=Lg.lang["InfoTabMenu"], menu=info_menu)

  about_message = "".join(Lg.lang["AboutMessage"])
  info_menu.add_command(label=Lg.lang["AboutMenuLabel"],
                        command=lambda: create_top_level(tk, about_message, Lg.lang["AboutMenuLabel"], 420, 270)
                        )

  credits_message = "".join(Lg.lang["CreditsMessage"])
  info_menu.add_command(label=Lg.lang["CreditsMenuLabel"],
                        command=lambda: create_top_level(tk, credits_message, Lg.lang["CreditsMenuLabel"], 400, 280)
                        )

def create_help_menu(tk, menu_widget):
  """Creates the help menu.
  
  Args:
    tk (tk): The tk library reference.
      Passed as argument to reduce double referencing on this file.
      Just a personal preference for this case
    menu_widget (tk.Widget): The menu widget where the menu is going to be attached
  """
  help_menu = tk.Menu(menu_widget, tearoff=0)
  menu_widget.add_cascade(label=Lg.lang["HelpTabMenu"], menu=help_menu)

  how_to_play_message = "".join(Lg.lang["HowToPlayMessage"])
  help_menu.add_command(label=Lg.lang["HowToPlayMenuLabel"],
                        command=lambda: create_top_level(tk, how_to_play_message, Lg.lang["HowToPlayMenuLabel"], 620, 440)
                        )

  rainbow_broccoli_message = "".join(Lg.lang["SpecialBroccolisMessage"])
  help_menu.add_command(label=Lg.lang["SpecialBroccolisMenuLabel"],
                        command=lambda: create_top_level(tk, rainbow_broccoli_message, Lg.lang["SpecialBroccolisMenuLabel"], 500, 350)
                        )