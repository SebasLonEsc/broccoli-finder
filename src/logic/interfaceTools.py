def centerWindow(window, windowWidth, windowHeight):
  screenWidth = window.winfo_screenwidth()
  screenHeight = window.winfo_screenheight()
  x = (screenWidth - windowWidth) // 2
  y = (screenHeight - windowHeight) // 2
  window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")