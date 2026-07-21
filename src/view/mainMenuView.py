import tkinter as tk
from functools import partial
from src.view.createNewGameView import createNewGameView
from src.logic.interfaceTools import centerWindow, closeInterface

def handleNewGame(root):
  closeInterface(root)
  createNewGameView(createMainMenuView)

def createMainMenuView():
  windowWidth = 220
  windowHeight = 80

  root = tk.Tk()
  root.title("Broccolis")
  root.minsize(windowWidth,windowHeight)
  root.maxsize(windowWidth,windowHeight)
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