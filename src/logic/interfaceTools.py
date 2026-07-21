def centerWindow(window, windowWidth, windowHeight):
  screenWidth = window.winfo_screenwidth()
  screenHeight = window.winfo_screenheight()
  x = (screenWidth - windowWidth) // 2
  y = (screenHeight - windowHeight) // 2
  window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

def closeInterface(root):
  root.destroy()

def goBack(root, goBackFunc, previousGoBackFunc = None):
  closeInterface(root)

  if previousGoBackFunc is None:
    goBackFunc()
  else:
    goBackFunc(previousGoBackFunc)