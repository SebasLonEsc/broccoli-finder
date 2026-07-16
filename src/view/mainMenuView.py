import tkinter as tk
from functools import partial
from src.view.createNewGameView import createNewGameView

def closeInterface(root):
  root.destroy()
  createNewGameView()

def handleNewGame(root):
  closeInterface(root)


def createMainMenuView():
  root = tk.Tk()
  root.title("Broccolis")
  tk.Label(
    root,
    text="Broccoli Seeker",
    anchor="center").grid(row=0, column=1, columnspan=3)
  
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
            ).grid(row=1, column=1, columnspan=3)
  
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
            ).grid(row=2, column=1, columnspan=3)
  
  root.mainloop()