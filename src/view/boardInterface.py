import tkinter as tk
import numpy as np
from functools import partial
from pathlib import Path
from PIL import Image, ImageTk

from src.logic.handleMove import handle_move
from src.logic.interfaceTools import close_interface, go_back, create_info_menu
from src.logic.constants.gameValues import WINNING_TEXT, LOSING_TEXT
from src.logic.constants.boardValues import BOARD_MAXIMUN_SIZE_PERCENT, TILE_PIXEL_SIZE
from src.logic.constants.styleValues import (BROCCOLI_COUNTER_COLOR,
                                             BROCCOLI_TILE_COLOR,
                                             BUTTON_ACTIVE_COLOR,
                                             BUTTON_COLOR,
                                             EATEN_BROCCOLI_TILE_COLOR,
                                             NULL_SPACE_TILE_COLOR,
                                             PROXIMITY_COLORS,
                                             TILE_BACKGROUND_COLOR
                                             )
from src.logic.constants.imagesPaths import (ACTIVE_FLAG_STATUS_IMAGE,
                                             FLAGGED_TILE_IMAGE,
                                             GREEN_BROCCOLI_BUTTON_IMAGE,
                                             GREEN_BROCCOLI_TILE_IMAGE,
                                             NULL_TILE_IMAGE,
                                             PROXIMITY_NUMBER_IMAGES,
                                             RED_BROCCOLI_TILE_IMAGE,
                                             TILE
                                             )

def changeFlagStatus(button):
  """Changes the current flag status for the game.

  When true the player can flag or unflag tiles, make moves otherwise.
  Args:
    button (tk.button): The button widget used for changing the status
  """
  global flagCommand
  image_name = FLAGGED_TILE_IMAGE

  if not flagCommand:
    image_name = ACTIVE_FLAG_STATUS_IMAGE

  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / image_name
  flagButtonImage = tk.PhotoImage(file=str(image_path))

  flagCommand = not flagCommand
  button.config(image=flagButtonImage)
  button.image = flagButtonImage

def handleFlagTile(board_object, buttons, move_position, broccoliCounter):
  """Handles the flaging or unflaging of a tile.
  
  Updates the tile images based on the status.
  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
    move_position (array): An array [row, column] of the current move made by the player
    broccoliCounter (tk.Label): Broccoli counter widget
  """
  global broccoliAmountCounter

  tiles_board = board_object.tiles_board
  row = move_position[0]
  column = move_position[1]
  clickedTile = tiles_board[row, column]

  if clickedTile["checked"]:
    return

  newFlaggedStatus = not clickedTile["flagged"]
  board_object.flag_tile(newFlaggedStatus, row, column)

  image_name = TILE

  if newFlaggedStatus:
    image_name = FLAGGED_TILE_IMAGE
    broccoliAmountCounter -= 1

  else:
    broccoliAmountCounter += 1

  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / image_name
  tileImage = tk.PhotoImage(file=str(image_path))

  buttons[row, column].config(image=tileImage)
  buttons[row, column].image = tileImage
  broccoliCounter.config(text=broccoliAmountCounter)

def handleGameStatus(board_object, buttons, move_position):
  """Updates the interface when winning or losing the game.

  Disables all buttons and reveal all broccolis if is a lost game.
  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
    move_position (array): An array [row, column] of the current move made by the player
  """
  tiles_board = board_object.tiles_board
  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / GREEN_BROCCOLI_TILE_IMAGE
  greenBroccoliImage = tk.PhotoImage(file=str(image_path))
  image_path = current_dir.parent / "images" / RED_BROCCOLI_TILE_IMAGE
  redBroccoliImage = tk.PhotoImage(file=str(image_path))

  for row in range(0, board_object.total_rows):
    for column in range(0, board_object.total_columns):
      checked = tiles_board[row, column]["checked"]
      isBroccoli = tiles_board[row, column]["tileValue"] == "-1"
      backgroundColor = BROCCOLI_TILE_COLOR

      buttons[row, column].config(command=lambda: None)

      broccoliImage = redBroccoliImage
      if move_position[0] == row and move_position[1] == column:
        backgroundColor = EATEN_BROCCOLI_TILE_COLOR
        broccoliImage = greenBroccoliImage

      if checked and isBroccoli:
        buttons[row, column].config(bg=backgroundColor,
                                    text="",
                                    image=broccoliImage
                                    )
        buttons[row, column].image = broccoliImage

def createProximityTileImages():
  """Creates an array of images for each proximity tile number

  Returns:
   array: An array of ImageTk.PhotoImage from 0 to 8 broccoli proximity tiles
  """
  current_dir = Path(__file__).parent
  tileImages = []

  for path in PROXIMITY_NUMBER_IMAGES:
    image_path = current_dir.parent / "images" / path
    image = Image.open(image_path)
    image = image.resize((24, 24), Image.Resampling.BOX)
    tileImage = ImageTk.PhotoImage(image, size=[24,24])
    tileImages.append(tileImage)

  return tileImages  


def handleText(board_object, buttons):
  """Updates the tiles of the board to show the tile value.

  The value can be empty, a proximity number or a broccoli.
  This applies for each affected tile by the player move
  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
  """
  tiles_board = board_object.tiles_board

  tileImages = createProximityTileImages()

  for row in range(0, board_object.total_rows):
    for column in range(0, board_object.total_columns):
      buttonColor = buttons[row, column].cget("bg")

      if buttonColor != TILE_BACKGROUND_COLOR:
        continue

      tileValue = 0
      if tiles_board[row, column]["tileValue"] != " ":
        tileValue = int(tiles_board[row, column]["tileValue"])

      buttonColor = PROXIMITY_COLORS[tileValue]
      checked = tiles_board[row, column]["checked"]

      if checked:
        buttons[row, column].config(bg=buttonColor,
                                    text="",
                                    command=lambda: None,
                                    image=tileImages[tileValue],
                                    )
        buttons[row, column].image = tileImages[tileValue]

def handleClick(board_object, buttons, move_position, winLabel, broccoliCounter):
  """Handles the click of the player on a tile of the board.

  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
    move_position (array): An array [row, column] of the current move made by the player
    winLabel (tk.Label): The label widget that shows the lose or win text
    broccoliCounter (tk.Label): Broccoli counter widget
  """
  tiles_board = board_object.tiles_board
  row = move_position[0]
  column = move_position[1]
  flagTileStatus = tiles_board[row, column]["flagged"]

  if not flagCommand and not flagTileStatus:
    board_object, game_status = handle_move(board_object, move_position)
    handleText(board_object, buttons)

    if game_status != 0:
      gameStatusText = WINNING_TEXT

      if game_status < 0:
        gameStatusText = LOSING_TEXT

      winLabel.config(text=gameStatusText)
      handleGameStatus(board_object, buttons, move_position)

  elif flagCommand:
    handleFlagTile(board_object, buttons, move_position, broccoliCounter)


def createBoardCanvas(root):
  """Creates a canvas to display the board on it.

  The canvas adds a scrollbar for big sized boards
  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
  Returns:
    tk.Frame: The frame where the board will be displayed
  """
  canvasFrame = tk.Frame(root)
  canvasFrame.pack(expand=True, fill="both")
  boardCanvas = tk.Canvas(canvasFrame)
  boardCanvas.pack(side="left", fill="both", expand=True, anchor="center")
  scrollbar = tk.Scrollbar(canvasFrame, orient="vertical", command=boardCanvas.yview)
  scrollbar.pack(side="right", fill="y")
  boardCanvas.configure(yscrollcommand=scrollbar.set)

  gameFrame = tk.Frame(boardCanvas)
  gameFrame.bind("<Configure>",
                 lambda _: boardCanvas.configure(scrollregion=boardCanvas.bbox("all")))
  canvasWindowId = boardCanvas.create_window((0,0), window=gameFrame, anchor="center")
  boardCanvas.bind("<Configure>",
                   lambda _: boardCanvas.itemconfig(canvasWindowId, width=canvasFrame.winfo_width()))

  return gameFrame

def create_board_interface(board_object, go_back_func, goToMainMenu):
  """Creates the interface of the board

  Args:
    board_object (Board): Rhe object containing all of the information about the board
    go_back_func (Func): Function to go back to the previous view
    goToMainMenu (Func): Function to go back to the main menu view
  """
  rows = board_object.total_rows
  columns = board_object.total_columns
  buttons = np.empty(shape=[rows, columns], dtype="object")
  tiles_board = board_object.tiles_board

  global broccoliAmountCounter
  broccoliAmountCounter = board_object.broccoli_amount

  global flagCommand
  flagCommand = False

  root = tk.Tk()
  root.title("Broccoli")
  root.grid_columnconfigure(0, weight=1)
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  root.maxsize(screen_width, screen_height)
  root.geometry("+%d+%d" % ((screen_width // 4), 0))

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  game_menu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label="Game", menu=game_menu)
  game_menu.add_command(label="Main Menu", command=partial(go_back, root, goToMainMenu))
  game_menu.add_command(label="New Game", command=partial(go_back, root, go_back_func, goToMainMenu))
  game_menu.add_separator()
  game_menu.add_command(label="Exit", command=partial(close_interface, root))
  create_info_menu(tk, menu)

  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / FLAGGED_TILE_IMAGE
  flagButtonImage = tk.PhotoImage(file=str(image_path))

  topFrameColumnSize = columns if columns > 10 else 10
  topFrameWidth = TILE_PIXEL_SIZE * topFrameColumnSize
  topFrame = tk.Frame(root, width=topFrameWidth, height=30, pady=2)
  topFrame.propagate(False)     # Allows to define the width and height of the frame
  topFrame.pack()
  button = tk.Button(topFrame,
                     activebackground="white",
                     anchor="center",
                     bd=0,
                     justify="center",
                     height=22,
                     width=22,
                     padx=0,
                     pady=0,
                     image=flagButtonImage
                     )

  button.config(command=partial(changeFlagStatus, button))
  button.image = flagButtonImage
  button.pack(side="left", expand=True)

  tk.Label(topFrame, text="Broccoli Finder").pack(side="left", expand=True)

  broccoliCounterFrame = tk.Frame(topFrame)
  broccoliCounterFrame.pack(side="right", expand=True)
  image_path = current_dir.parent / "images" / GREEN_BROCCOLI_BUTTON_IMAGE
  broccoliCounterImage = tk.PhotoImage(file=str(image_path))
  broccoliCounterLabel = tk.Label(broccoliCounterFrame,
                                  bg=BUTTON_COLOR,
                                  image=broccoliCounterImage,
                                  bd=2,
                                  relief="raised"
                                  )
  broccoliCounterLabel.image = broccoliCounterImage
  broccoliCounterLabel.pack(side="left", padx=[2,2])

  emptyImage = tk.PhotoImage(file="", width=1, height=1)
  broccoliCounter = tk.Label(broccoliCounterFrame,
                             bd=2,
                             relief="raised",
                             bg=BROCCOLI_COUNTER_COLOR,
                             text=broccoliAmountCounter,
                             foreground="white",
                             height=22,
                             width=40,
                             justify="right",
                             compound="center",
                             image=emptyImage
                             )
  broccoliCounter.image = emptyImage
  broccoliCounter.pack(side="left")
  
  
  lastFrame= tk.Frame(root)
  gameStatuslabel = tk.Label(lastFrame, text="", anchor="center")

  gameFrame = tk.Frame(root, bd=2)
  boardCalculatedSize = rows * TILE_PIXEL_SIZE
  createCanvas = (boardCalculatedSize*100 / screen_height) > BOARD_MAXIMUN_SIZE_PERCENT
  if(createCanvas):
    gameFrame = createBoardCanvas(root)
  else:
    gameFrame.pack()

  image_path = current_dir.parent / "images" / TILE
  tileImage = tk.PhotoImage(file=str(image_path))
  image_path = current_dir.parent / "images" / NULL_TILE_IMAGE
  NullTileImage = tk.PhotoImage(file=str(image_path))
  
  for row in range(0, rows):
    frame = tk.Frame(gameFrame, bg=TILE_BACKGROUND_COLOR)
    frame.pack()

    for column in range(0, columns):
      isNullSpace = tiles_board[row, column]["checked"]
      backgroundColor = TILE_BACKGROUND_COLOR
      buttonCommand = partial(handleClick,
                              board_object,
                              buttons,
                              [row, column],
                              gameStatuslabel,
                              broccoliCounter
                              )

      if isNullSpace:
        buttonCommand = lambda: None
        backgroundColor = NULL_SPACE_TILE_COLOR

      button = tk.Button(frame,
                         activebackground="white",
                         anchor="center",
                         bd=0,
                         bg=backgroundColor,
                         command=buttonCommand,
                         disabledforeground="white",
                         justify="center",
                         height=22,
                         width=22,
                         padx=0,
                         pady=0,
                         image=tileImage if not isNullSpace else NullTileImage,
                         compound="center"
                         )
            
      buttons[row, column] = button
      button.pack(side="left")
      button = None

  lastFrame.pack()
  gameStatuslabel.pack()

  actionFrame = tk.Frame(root)
  actionFrame.pack(pady=[0,2])
  tk.Button(actionFrame,
            activebackground=BUTTON_ACTIVE_COLOR,
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(go_back, root, goToMainMenu),
            justify="center",
            height=1,
            padx=0,
            pady=0,
            text="Main Menu",
            ).pack(side="left", padx=[2,4])
  
  tk.Button(actionFrame,
            activebackground=BUTTON_ACTIVE_COLOR,
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(close_interface, root),
            justify="center",
            height=1,
            width=8,
            padx=0,
            pady=0,
            text="Exit",
            ).pack(side="left", padx=[4,2])
  
  root.mainloop()
