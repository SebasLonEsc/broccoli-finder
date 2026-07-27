import tkinter as tk
import numpy as np
from functools import partial
from pathlib import Path
from PIL import Image, ImageTk
from src.logic.handleMove import handleMove
from src.logic.constants.gameValues import *
from src.logic.constants.boardValues import BOARDMAXIMUNSIZEPERCENT, TILEPIXELHEIGHT
from src.logic.constants.styleValues import *
from src.logic.constants.imagesPaths import PROXIMITYNUMBERIMAGES
from src.logic.interfaceTools import closeInterface, goBack

# Updates the interface when winning or losing the game
# Disables all buttons and reveal all broccolis if is a lost game
# Input:
#   boardObject: the object containing all of the information about the board
#   buttons: a matrix contains all of the buttons that correspond to each tile on the board in the interface
#   movePosition: an array containg the [row, column] of the current move made by the player
# Output:
#   Nothing
def handleGameStatus(boardObject, buttons, movePosition):
  tilesBoard = boardObject.tilesBoard
  currentDir = Path(__file__).parent
  imagePath = currentDir.parent / "images" / "Green_broccoli.png"
  greenBroccoliImage = tk.PhotoImage(file = str(imagePath))
  imagePath = currentDir.parent / "images" / "Red_broccoli.png"
  redBroccoliImage = tk.PhotoImage(file = str(imagePath))

  for row in range(0, boardObject.totalRows):
    for column in range(0, boardObject.totalColumns):
      checked = tilesBoard[row, column]["checked"]
      isBroccoli = tilesBoard[row, column]["tileValue"] == "-1"
      backgroundColor = BROCCOLITILECOLOR

      buttons[row, column].config(command=lambda: None)

      broccoliImage = redBroccoliImage
      if movePosition[0] == row and movePosition[1] == column:
        backgroundColor = EATENBROCCOLITILECOLOR
        broccoliImage = greenBroccoliImage

      if checked and isBroccoli:
        buttons[row, column].config(bg=backgroundColor,
                                    text="",
                                    image=broccoliImage)
        buttons[row, column].image = broccoliImage

# Creates an array of images for each proximity tile number
# Input:
#   Nothing
# Output:
#   Array [PhotoImage, PhotoImage...]: An array from 0 to 8 broccoli proximity tile images
def createProximityTileImages():
  currentDir = Path(__file__).parent
  tileImages = []

  for path in PROXIMITYNUMBERIMAGES:
    imagePath = currentDir.parent / "images" / path
    image = Image.open(imagePath)
    image = image.resize((24, 24), Image.Resampling.BOX)
    tileImage = ImageTk.PhotoImage(image, size=[24,24])
    tileImages.append(tileImage)

  return tileImages  

# Updates the tiles of the board to show the value (empty, proximity number or broccoli) of each affected tile by the player move
# Input:
#   boardObject: the object containing all of the information about the board
#   buttons: a matrix contains all of the buttons that correspond to each tile on the board in the interface
# Output:
#   Nothing
def handleText(boardObject, buttons):
  tilesBoard = boardObject.tilesBoard

  tileImages = createProximityTileImages()

  for row in range(0, boardObject.totalRows):
    for column in range(0, boardObject.totalColumns):
      buttonColor = buttons[row, column].cget("bg")

      if buttonColor != TILEBACKGROUNDCOLOR:
        continue

      tileValue = 0
      if tilesBoard[row, column]["tileValue"] != " ":
        tileValue = int(tilesBoard[row, column]["tileValue"])

      buttonColor = PROXIMITYCOLORS[tileValue]
      checked = tilesBoard[row, column]["checked"]

      if checked:
        buttons[row, column].config(bg=buttonColor,
                                    text="",
                                    command=lambda: None,
                                    image=tileImages[tileValue],
                                    )
        buttons[row, column].image = tileImages[tileValue]

# Handles the click of the player on a tile of the board
# Input:
#   boardObject: the object containing all of the information about the board
#   buttons: a matrix contains all of the buttons that correspond to each tile on the board in the interface
#   movePosition: an array containg the [row, column] of the current move made by the player
#   winLabel: the label widget that shows the lose or win text
# Output:
#   Nothing
def handleClick(boardObject, buttons, movePosition, winLabel):
  boardObject, gameStatus = handleMove(boardObject, movePosition)
  handleText(boardObject, buttons)

  if gameStatus != 0:
    gameStatusText = WINNINGTEXT

    if gameStatus < 0:
      gameStatusText = LOSINGTEXT

    winLabel.config(text=gameStatusText)
    handleGameStatus(boardObject, buttons, movePosition)

# Creates a canvas to display the board on it
# The canvas add a scrollbar for big sized boards
# Input:
#   root: the root windget, the current window that is being displayed
# Output:
#   tk.Frame: The frame where the board will be displayed
def createBoardCanvas(root):
  canvasFrame = tk.Frame(root)
  canvasFrame.pack(expand=True, fill="both")
  boardCanvas = tk.Canvas(canvasFrame)
  boardCanvas.pack(side="left", fill="both", expand=True, anchor="center")
  scrollbar = tk.Scrollbar(canvasFrame, orient="vertical", command=boardCanvas.yview)
  scrollbar.pack(side="right", fill="y")
  boardCanvas.configure(yscrollcommand=scrollbar.set)

  gameFrame = tk.Frame(boardCanvas)
  gameFrame.bind("<Configure>", lambda e: boardCanvas.configure(scrollregion=boardCanvas.bbox("all")))
  canvasWindowId = boardCanvas.create_window((0,0), window=gameFrame, anchor="center")
  boardCanvas.bind("<Configure>", lambda e: boardCanvas.itemconfig(canvasWindowId, width=canvasFrame.winfo_width()))

  return gameFrame

# Creates the interface of the board
# Input:
#   boardObject: the object containing all of the information about the board
#   goBackFunc: Function to go back to the previous view
#   goToMainMenu: Function to go back to the main menu view
# Output:
#   Nothing
def createBoardInterface(boardObject, goBackFunc, goToMainMenu):
  rows = boardObject.totalRows
  columns = boardObject.totalColumns
  buttons = np.empty(shape=[rows,columns],dtype="object")
  tilesBoard = boardObject.tilesBoard

  root = tk.Tk()
  root.title("Broccoli")
  root.grid_columnconfigure(0, weight=1)
  screenWidth = root.winfo_screenwidth()
  screenHeight = root.winfo_screenheight()
  root.maxsize(screenWidth, screenHeight)
  root.geometry("+%d+%d" % ((screenWidth // 4), 0))

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  gameMenu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label="Game", menu=gameMenu)
  gameMenu.add_command(label="Main Menu", command=partial(goBack, root, goToMainMenu))
  gameMenu.add_command(label="New Game", command=partial(goBack, root, goBackFunc, goToMainMenu))
  gameMenu.add_separator()
  gameMenu.add_command(label="Exit", command=partial(closeInterface, root))

  frame = tk.Frame(root)
  frame.pack()
  tk.Label(frame, text="Broccoli Seeker").pack()
  
  lastFrame= tk.Frame(root)
  gameStatuslabel = tk.Label(lastFrame, text="", anchor="center")

  gameFrame = tk.Frame(root, bd=2)
  createCanvas = (rows * TILEPIXELHEIGHT * 100) / screenHeight > BOARDMAXIMUNSIZEPERCENT  
  if(createCanvas):
    gameFrame = createBoardCanvas(root)
  else:
    gameFrame.pack()

  currentDir = Path(__file__).parent
  imagePath = currentDir.parent / "images" / "Tile.png"
  tileImage = tk.PhotoImage(file=str(imagePath))
  imagePath = currentDir.parent / "images" / "Null_Tile.png"
  NullTileImage = tk.PhotoImage(file=str(imagePath))
  
  for row in range(0, rows):
    frame = tk.Frame(gameFrame, bg=TILEBACKGROUNDCOLOR)
    frame.pack()

    for column in range(0, columns):
      isNullSpace = tilesBoard[row, column]["checked"]
      backgroundColor = TILEBACKGROUNDCOLOR
      buttonCommand = partial(handleClick, boardObject, buttons, [row, column], gameStatuslabel)

      if isNullSpace:
        buttonCommand = lambda: None
        backgroundColor = NULLSPACETILECOLOR

      button = tk.Button(frame,
                        activebackground="white",
                        anchor="center",
                        bd=0,
                        bg=backgroundColor,
                        command= buttonCommand,
                        disabledforeground="white",
                        justify="center",
                        height=22,
                        width=22,
                        padx=0,
                        pady=0,
                        image=tileImage if not isNullSpace else NullTileImage,
                        compound="center",
                        )
            
      buttons[row, column] = button
      button.pack(side="left")
      button = None

  lastFrame.pack()
  gameStatuslabel.pack()

  actionFrame = tk.Frame(root)
  actionFrame.pack(pady=[0,2])
  tk.Button(actionFrame,
            activebackground=BUTTONACTIVECOLOR,
            anchor="center",
            bd=1,
            bg=BUTTONCOLOR,
            command= partial(goBack, root, goToMainMenu),
            justify="center",
            height=1,
            padx=0,
            pady=0,
            text= "Main Menu",
            ).pack(side="left", padx=[2,4])
  tk.Button(actionFrame,
            activebackground=BUTTONACTIVECOLOR,
            anchor="center",
            bd=1,
            bg=BUTTONCOLOR,
            command= partial(closeInterface, root),
            justify="center",
            height=1,
            width=8,
            padx=0,
            pady=0,
            text= "Exit",
            ).pack(side="left", padx=[4,2])
  
  root.mainloop()
