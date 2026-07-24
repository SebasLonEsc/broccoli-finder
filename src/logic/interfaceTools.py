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
#   goBackFunc: The current goBack function. Used to go back to the previous view
#   previousGoBackFunc (optional): The goBack function of the previous view. Used to go back two views prior
# Output:
#   Nothing
def goBack(root, goBackFunc, previousGoBackFunc = None):
  closeInterface(root)

  if previousGoBackFunc is None:
    goBackFunc()
  else:
    goBackFunc(previousGoBackFunc)