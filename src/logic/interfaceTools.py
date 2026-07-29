from src.logic.constants.infoMenuContent import CREDITSMENUMESSAGE, ABOUTMENUMESSAGE

# Closes the current window
# Input:
#   window: the root windget, the current window that is being displayed
#   windowWidth: the width of the current window
#   windowHeight: the height of the current window
# Output:
#   Nothing
def centerWindow(window, windowWidth, windowHeight):
  screenWidth = window.winfo_screenwidth()
  screenHeight = window.winfo_screenheight()
  x = (screenWidth - windowWidth) // 2
  y = (screenHeight - windowHeight) // 2
  window.geometry("+%d+%d" % (x, y))

# Closes the current window
# Input:
#   root: the root windget, the current window that is being displayed
# Output:
#   Nothing
def closeInterface(root):
  root.destroy()

# Closes the current window and creates the new game menu window
# Input:
#   root: the root windget, the current window that is being displayed
#   goBackFunc: The current goBack function.
#     Used to go back to the previous view
#   previousGoBackFunc(optional): The goBack function of the previous view.
#     Used to go back two views prior
# Output:
#   Nothing
def goBack(root, goBackFunc, previousGoBackFunc = None):
  closeInterface(root)

  if previousGoBackFunc is None:
    goBackFunc()
  else:
    goBackFunc(previousGoBackFunc)

# Creates a toplevel widget with a message and title
# Input:
#   tk: The tk library reference
#     (passed as argument to reduce double referencing on this file.
#      Just a personal preference for this case)
#   message: The message to be displayed on the toplevel
#   title: The title of the toplevel
# Output:
#   Nothing
def createTopLevel(tk, message, title):
  topLevel = tk.Toplevel()
  topLevel.title(title)
  topLevel.geometry("400x250")

  messageWidget = tk.Message(topLevel, text = message)
  closeButton = tk.Button(topLevel,
                          text = "Close",
                          command = topLevel.destroy
                          )

  messageWidget.pack()
  closeButton.pack(pady=[2,0])
  topLevel.mainloop()

# Creates the info menu
# Input:
#   tk: The tk library reference
#     (passed as argument to reduce double referencing on this file.
#      Just a personal preference for this case)
#   menuWidget: The menu widget where the menu is going to be attached
# Output:
#   Nothing
def createInfoMenu(tk, menuWidget):
  aboutMessage = "".join(ABOUTMENUMESSAGE)
  creditsMessage = "".join(CREDITSMENUMESSAGE)

  infoMenu = tk.Menu(menuWidget, tearoff=0)
  menuWidget.add_cascade(label="Info", menu=infoMenu)

  infoMenu.add_command(label="About",
                       command=lambda: createTopLevel(tk, aboutMessage, "About")
                       )
  infoMenu.add_command(label="Credits",
                       command=lambda: createTopLevel(tk, creditsMessage, "Credits")
                       )
