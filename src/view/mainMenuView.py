import tkinter as tk
from functools import partial
from src.view.newGameMenu import newGameMenu
from src.logic.interfaceTools import centerWindow, closeInterface

# Closes the current window and creates the new game menu window
# Input:
#   root: the root windget, the current window that is being displayed
# Output:
#   Nothing
def handleNewGame(root):
  closeInterface(root)
  newGameMenu(createMainMenuView)

# Creates the main menu window
# Input:
#   Nothing
# Output:
#   Nothing
def createMainMenuView():
  windowWidth = 220
  windowHeight = 80

  root = tk.Tk()
  root.title("Broccolis")
  root.minsize(windowWidth, windowHeight)
  root.maxsize(windowWidth, windowHeight)
  centerWindow(root, windowWidth, windowHeight)

  tk.Label(
    root,
    text="Broccoli Seeker",
    anchor="center").pack(pady=2)
  
  tk.Button(root,
            activebackground="white",
            anchor="center",
            bd=1,
            bg="lightgray",
            command= partial(handleNewGame, root),
            disabledforeground="white",
            justify="center",
            height=1,
            padx=0,
            pady=0,
            text= "New Game",
            ).pack(pady=2)
  
  tk.Button(root,
            activebackground="white",
            anchor="center",
            bd=1,
            bg="lightgray",
            command= partial(closeInterface, root),
            disabledforeground="white",
            justify="center",
            height=1,
            width=8,
            padx=0,
            pady=0,
            text= "Exit",
            ).pack(pady=[4,8])
  
  root.mainloop()