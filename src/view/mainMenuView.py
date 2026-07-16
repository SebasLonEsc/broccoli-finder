import tkinter as tk
from functools import partial
from src.view.createNewGameView import createNewGameView

def closeInterface(root):
  root.destroy()

def handleNewGame(root):
  closeInterface(root)
  createNewGameView()


def createMainMenuView():
  root = tk.Tk()
  root.title("Broccolis")
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
            padx=0,
            pady=0,
            text= "Exit",
            ).pack(pady=[4,8])
  
  root.mainloop()