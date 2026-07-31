from src.logic.constants.infoMenuContent import CREDITS_MENU_MESSAGE, ABOUT_MENU_MESSAGE

def centerWindow(window, windowWidth, windowHeight):
  """Places the window at the center of the screen.

  Args:
    window (tk.widget): The root windget, the current window that is being displayed
    windowWidth (int): The width of the current window
    windowHeight (int): The height of the current window
  """
  screenWidth = window.winfo_screenwidth()
  screenHeight = window.winfo_screenheight()
  x = (screenWidth - windowWidth) // 2
  y = (screenHeight - windowHeight) // 2
  window.geometry("+%d+%d" % (x, y))

def closeInterface(root):
  """Closes the current window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
  """
  root.destroy()

def goBack(root, goBackFunc, previousGoBackFunc=None):
  """Closes the current window and creates the new game menu window.

  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
    goBackFunc (Func): The current goBack function.
      Used to go back to the previous view
    previousGoBackFunc (Func): The goBack function of the previous view.
      Used to go back two views prior (default None)
  """
  closeInterface(root)

  if previousGoBackFunc is None:
    goBackFunc()
  else:
    goBackFunc(previousGoBackFunc)

def createTopLevel(tk, message, title):
  """Creates a toplevel widget with a message and title.

  Args:
    tk (tk): The tk library reference
      (passed as argument to reduce double referencing on this file.
      Just a personal preference for this case)
    message (str): The message to be displayed on the toplevel
    title (str): The title of the toplevel
  """
  topLevel = tk.Toplevel()
  topLevel.title(title)
  topLevel.geometry("400x250")

  messageWidget = tk.Message(topLevel, text=message)
  closeButton = tk.Button(topLevel,
                          text="Close",
                          command=topLevel.destroy
                          )

  messageWidget.pack()
  closeButton.pack(pady=[2,0])
  topLevel.mainloop()

def createInfoMenu(tk, menuWidget):
  """Creates the info menu.

  Args:
    tk (tk): The tk library reference.
      Passed as argument to reduce double referencing on this file.
      Just a personal preference for this case
    menuWidget (tk.Widget): The menu widget where the menu is going to be attached
  """
  aboutMessage = "".join(ABOUT_MENU_MESSAGE)
  creditsMessage = "".join(CREDITS_MENU_MESSAGE)

  infoMenu = tk.Menu(menuWidget, tearoff=0)
  menuWidget.add_cascade(label="Info", menu=infoMenu)

  infoMenu.add_command(label="About",
                       command=lambda: createTopLevel(tk, aboutMessage, "About")
                       )
  infoMenu.add_command(label="Credits",
                       command=lambda: createTopLevel(tk, creditsMessage, "Credits")
                       )
