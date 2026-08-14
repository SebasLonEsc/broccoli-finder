import random
import tkinter as tk
import numpy as np
from functools import partial
from pathlib import Path
from PIL import Image, ImageTk

import src.lang.language as Lg
from src.logic.handleMove import handle_move
from src.logic.interfaceTools import close_interface, go_back, create_info_menu
from src.logic.constants.gameValues import get_winning_text, get_losing_text
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
                                             TILE,
                                             FLOWERING_BROCCOLI_TILE_IMAGE,
                                             RAINBOW_BROCCOLI_TILE_IMAGE,
                                             RAINBOW_PROXIMITY_NUMBER_IMAGES
                                             )

def change_flag_status(button):
  """Changes the current flag status for the game.

  When true the player can flag or unflag tiles, make moves otherwise.
  Args:
    button (tk.button): The button widget used for changing the status
  """
  global flag_command
  image_name = FLAGGED_TILE_IMAGE

  if not flag_command:
    image_name = ACTIVE_FLAG_STATUS_IMAGE

  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / image_name
  flag_button_image = tk.PhotoImage(file=str(image_path))

  flag_command = not flag_command
  button.config(image=flag_button_image)
  button.image = flag_button_image

def handle_flag_tile(board_object, buttons, move_position, broccoli_counter):
  """Handles the flaging or unflaging of a tile.
  
  Updates the tile images based on the status.
  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
    move_position (array): An array [row, column] of the current move made by the player
    broccoli_counter (tk.Label): Broccoli counter widget
  """
  global broccoli_counter_value

  tiles_board = board_object.tiles_board
  row = move_position[0]
  column = move_position[1]
  clicked_tile = tiles_board[row, column]

  if clicked_tile["checked"]:
    return

  new_flagged_status = not clicked_tile["flagged"]
  board_object.flag_tile(new_flagged_status, row, column)

  image_name = TILE

  if new_flagged_status:
    image_name = FLAGGED_TILE_IMAGE
    broccoli_counter_value -= 1

  else:
    broccoli_counter_value += 1

  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / image_name
  tile_image = tk.PhotoImage(file=str(image_path))

  buttons[row, column].config(image=tile_image)
  buttons[row, column].image = tile_image
  broccoli_counter.config(text=broccoli_counter_value)

def handle_game_status(board_object, buttons, move_position):
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
  green_broccoli_image = tk.PhotoImage(file=str(image_path))
  image_path = current_dir.parent / "images" / RED_BROCCOLI_TILE_IMAGE
  red_broccoli_image = tk.PhotoImage(file=str(image_path))
  image_path = current_dir.parent / "images" / RAINBOW_BROCCOLI_TILE_IMAGE
  rainbow_broccoli_image = tk.PhotoImage(file=str(image_path))

  for row in range(0, board_object.total_rows):
    for column in range(0, board_object.total_columns):
      checked = tiles_board[row, column]["checked"]
      is_broccoli = (tiles_board[row, column]["tileValue"] == "-1" or
                     tiles_board[row, column]["tileValue"] == "-3")
      is_rainbow_broccoli = tiles_board[row, column]["tileValue"] == "-3"
      background_color = BROCCOLI_TILE_COLOR

      buttons[row, column].config(command=lambda: None)

      broccoli_image = red_broccoli_image
      if move_position[0] == row and move_position[1] == column:
        background_color = EATEN_BROCCOLI_TILE_COLOR
        broccoli_image = green_broccoli_image

      if is_rainbow_broccoli:
        broccoli_image = rainbow_broccoli_image

      if checked and is_broccoli:
        buttons[row, column].config(bg=background_color,
                                    text="",
                                    image=broccoli_image
                                    )
        buttons[row, column].image = broccoli_image

def create_proximity_tile_images(images_array):
  """Creates an array of images for each proximity tile number

  Returns:
   array: An array of ImageTk.PhotoImage from 0 to 8 broccoli proximity tiles
  """
  current_dir = Path(__file__).parent
  tile_images = []

  for path in images_array:
    image_path = current_dir.parent / "images" / path
    image = Image.open(image_path)
    image = image.resize((TILE_PIXEL_SIZE, TILE_PIXEL_SIZE), Image.Resampling.BOX)
    tile_image = ImageTk.PhotoImage(image, size=[TILE_PIXEL_SIZE, TILE_PIXEL_SIZE])
    tile_images.append(tile_image)

  return tile_images  


def handle_revealed_tiles(board_object, buttons):
  """Updates the tiles of the board to show the tile value.

  The value can be empty, a proximity number or a broccoli.
  This applies for each affected tile by the player move
  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
  """
  tiles_board = board_object.tiles_board

  tile_images = create_proximity_tile_images(PROXIMITY_NUMBER_IMAGES)
  rainbow_tile_images = create_proximity_tile_images(RAINBOW_PROXIMITY_NUMBER_IMAGES)

  for row in range(0, board_object.total_rows):
    for column in range(0, board_object.total_columns):
      button_color = buttons[row, column].cget("bg")

      if button_color != TILE_BACKGROUND_COLOR:
        continue

      tile_value = 0
      if tiles_board[row, column]["tileValue"] != " ":
        tile_value = int(tiles_board[row, column]["tileValue"])

      checked = tiles_board[row, column]["checked"]

      if checked:
        image = tile_images[0]
        button_color = PROXIMITY_COLORS[0]

        if tile_value >= 0 and tile_value <= 8:
          button_color = PROXIMITY_COLORS[tile_value]
          image = tile_images[tile_value]

        if tile_value >= 11 and tile_value <= 18:
          # Index for rainbow tile images is the tile value minus 11
          # Because tile value is 10 times more and 
          # empty tile don't exist in rainbow proximity numbers
          image = rainbow_tile_images[tile_value-11]
          button_color = PROXIMITY_COLORS[tile_value-10] # Array has +1 index for empty tile

        buttons[row, column].config(bg=button_color,
                                    text="",
                                    command=lambda: None,
                                    image=image,
                                    )
        buttons[row, column].image = image

def handle_rainbow_broccoli_reveal(board_object, buttons, move_position, broccoli_counter):
  """Reveals the rainbow and flowering broccoli tiles

  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
    move_position (array): An array [row, column] of the current move made by the player
    broccoli_counter (tk.Label): Broccoli counter widget
  """
  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / RAINBOW_BROCCOLI_TILE_IMAGE
  rainbow_broccoli_image = tk.PhotoImage(file=str(image_path))

  buttons[move_position[0], move_position[1]].config(bg=PROXIMITY_COLORS[0],
                                                     text="",
                                                     command=lambda: None,
                                                     image=rainbow_broccoli_image,
                                                     )
  buttons[move_position[0], move_position[1]].image = rainbow_broccoli_image

  broccoli_positions = board_object.broccoli_positions
  board = board_object.board
  invalid_position = True
  pos = []

  if len(broccoli_positions) == 1:
    invalid_position = False
    pos = broccoli_positions[0]

  while invalid_position:
    pos_index = random.randrange(0, len(broccoli_positions))
    pos = broccoli_positions[pos_index]

    if board[pos[0], pos[1]] == -4:
      invalid_position = False

  image_path = current_dir.parent / "images" / FLOWERING_BROCCOLI_TILE_IMAGE
  flowering_broccoli_image = tk.PhotoImage(file=str(image_path))

  buttons[pos[0], pos[1]].config(bg=PROXIMITY_COLORS[0],
                                 text="",
                                 command=lambda: None,
                                 image=flowering_broccoli_image,
                                 )
  buttons[pos[0], pos[1]].image = flowering_broccoli_image

  global broccoli_counter_value
  broccoli_counter_value -= 2

  if board_object.tiles_board[pos[0], pos[1]]["flagged"] == True:
    broccoli_counter_value +=1

  broccoli_counter.config(text=broccoli_counter_value)


def handle_click(board_object, buttons, move_position, win_label, broccoli_counter):
  """Handles the click of the player on a tile of the board.

  Args:
    board_object (Board): The object containing all of the information about the board
    buttons (np.ndarray): A matrix in the shape [[tk.button, tk.button], [tk.button]].
      Contains all of the buttons in the board, each one correspond to a tile on the board in the interface
    move_position (array): An array [row, column] of the current move made by the player
    win_label (tk.Label): The label widget that shows the lose or win text
    broccoli_counter (tk.Label): Broccoli counter widget
  """
  tiles_board = board_object.tiles_board
  row = move_position[0]
  column = move_position[1]
  flag_tile_status = tiles_board[row, column]["flagged"]

  if not flag_command and not flag_tile_status:
    board_object, game_status = handle_move(board_object, move_position)
    handle_revealed_tiles(board_object, buttons)
    board = board_object.board

    if board[move_position[0], move_position[1]] == -3:
      handle_rainbow_broccoli_reveal(board_object, buttons, move_position, broccoli_counter)

    if game_status != 0:
      game_status_text = get_winning_text()

      if game_status < 0:
        game_status_text = get_losing_text()

      win_label.config(text=game_status_text)
      handle_game_status(board_object, buttons, move_position)

  elif flag_command:
    handle_flag_tile(board_object, buttons, move_position, broccoli_counter)


def create_board_canvas(root):
  """Creates a canvas to display the board on it.

  The canvas adds a scrollbar for big sized boards
  Args:
    root (tk.Tk): The root windget, the current window that is being displayed
  Returns:
    tk.Frame: The frame where the board will be displayed
  """
  canvas_frame = tk.Frame(root)
  canvas_frame.pack(expand=True, fill="both")
  board_canvas = tk.Canvas(canvas_frame)
  board_canvas.pack(side="left", fill="both", expand=True, anchor="center")
  scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=board_canvas.yview)
  scrollbar.pack(side="right", fill="y")
  board_canvas.configure(yscrollcommand=scrollbar.set)

  game_frame = tk.Frame(board_canvas)
  game_frame.bind("<Configure>",
                 lambda _: board_canvas.configure(scrollregion=board_canvas.bbox("all")))
  canvas_window_id = board_canvas.create_window((0,0), window=game_frame, anchor="center")
  board_canvas.bind("<Configure>",
                   lambda _: board_canvas.itemconfig(canvas_window_id, width=canvas_frame.winfo_width()))

  return game_frame

def create_board_interface(board_object, go_back_func, go_to_main_menu):
  """Creates the interface of the board

  Args:
    board_object (Board): Rhe object containing all of the information about the board
    go_back_func (Func): Function to go back to the previous view
    go_to_main_menu (Func): Function to go back to the main menu view
  """
  rows = board_object.total_rows
  columns = board_object.total_columns
  buttons = np.empty(shape=[rows, columns], dtype="object")
  tiles_board = board_object.tiles_board

  global broccoli_counter_value
  broccoli_counter_value = board_object.broccoli_amount

  global flag_command
  flag_command = False

  root = tk.Tk()
  root.title(Lg.lang["GameTitle"])
  root.grid_columnconfigure(0, weight=1)
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  root.maxsize(screen_width, screen_height)
  root.geometry("+%d+%d" % ((screen_width // 4), 0))

  menu = tk.Menu(root, tearoff=0)
  root.config(menu=menu)
  game_menu = tk.Menu(menu, tearoff=0)
  menu.add_cascade(label=Lg.lang["GameTabMenu"], menu=game_menu)
  game_menu.add_command(label=Lg.lang["MainMenuLabel"], command=partial(go_back, root, go_to_main_menu))
  game_menu.add_command(label=Lg.lang["NewGameLabel"], command=partial(go_back, root, go_back_func, go_to_main_menu))
  game_menu.add_separator()
  game_menu.add_command(label=Lg.lang["Exit"], command=partial(close_interface, root))
  create_info_menu(tk, menu)

  current_dir = Path(__file__).parent
  image_path = current_dir.parent / "images" / FLAGGED_TILE_IMAGE
  flag_button_image = tk.PhotoImage(file=str(image_path))

  top_frame_column_size = columns if columns > 10 else 10
  top_frame_width = TILE_PIXEL_SIZE * top_frame_column_size
  top_frame = tk.Frame(root, width=top_frame_width, height=30, pady=2)
  top_frame.propagate(False)     # Allows to define the width and height of the frame
  top_frame.pack()
  button = tk.Button(top_frame,
                     activebackground="white",
                     anchor="center",
                     bd=0,
                     justify="center",
                     height=22,
                     width=22,
                     padx=0,
                     pady=0,
                     image=flag_button_image
                     )

  button.config(command=partial(change_flag_status, button))
  button.image = flag_button_image
  button.pack(side="left", expand=True)

  tk.Label(top_frame, text=Lg.lang["GameTitle"]).pack(side="left", expand=True)

  broccoli_counter_frame = tk.Frame(top_frame)
  broccoli_counter_frame.pack(side="right", expand=True)
  image_path = current_dir.parent / "images" / GREEN_BROCCOLI_BUTTON_IMAGE
  broccoli_counter_image = tk.PhotoImage(file=str(image_path))
  broccoli_counter_label = tk.Label(broccoli_counter_frame,
                                    bg=BUTTON_COLOR,
                                    image=broccoli_counter_image,
                                    bd=2,
                                    relief="raised"
                                    )
  broccoli_counter_label.image = broccoli_counter_image
  broccoli_counter_label.pack(side="left", padx=[2,2])

  empty_image = tk.PhotoImage(file="", width=1, height=1)
  broccoli_counter = tk.Label(broccoli_counter_frame,
                              bd=2,
                              relief="raised",
                              bg=BROCCOLI_COUNTER_COLOR,
                              text=broccoli_counter_value,
                              foreground="white",
                              height=22,
                              width=40,
                              justify="right",
                              compound="center",
                              image=empty_image
                              )
  broccoli_counter.image = empty_image
  broccoli_counter.pack(side="left")
  
  
  last_frame= tk.Frame(root)
  game_status_label = tk.Label(last_frame, text="", anchor="center")

  game_frame = tk.Frame(root, bd=2)
  board_calculated_size = rows * TILE_PIXEL_SIZE
  canvas_required = (board_calculated_size*100 / screen_height) > BOARD_MAXIMUN_SIZE_PERCENT
  if(canvas_required):
    game_frame = create_board_canvas(root)
  else:
    game_frame.pack()

  image_path = current_dir.parent / "images" / TILE
  tile_image = tk.PhotoImage(file=str(image_path))

  image_path = current_dir.parent / "images" / NULL_TILE_IMAGE
  null_tile_image = tk.PhotoImage(file=str(image_path))
  
  for row in range(0, rows):
    frame = tk.Frame(game_frame, bg=TILE_BACKGROUND_COLOR)
    frame.pack()

    for column in range(0, columns):
      is_null_space = tiles_board[row, column]["checked"]
      background_color = TILE_BACKGROUND_COLOR
      button_command = partial(handle_click,
                               board_object,
                               buttons,
                               [row, column],
                               game_status_label,
                               broccoli_counter
                               )

      if is_null_space:
        button_command = lambda: None
        background_color = NULL_SPACE_TILE_COLOR

      button = tk.Button(frame,
                         activebackground="white",
                         anchor="center",
                         bd=0,
                         bg=background_color,
                         command=button_command,
                         disabledforeground="white",
                         justify="center",
                         height=TILE_PIXEL_SIZE-2,
                         width=TILE_PIXEL_SIZE-2,
                         padx=0,
                         pady=0,
                         image=null_tile_image if is_null_space else tile_image,
                         compound="center"
                         )
            
      buttons[row, column] = button
      button.pack(side="left")
      button = None

  last_frame.pack()
  game_status_label.pack()

  action_frame = tk.Frame(root)
  action_frame.pack(pady=[0,2])
  tk.Button(action_frame,
            activebackground=BUTTON_ACTIVE_COLOR,
            anchor="center",
            bd=1,
            bg=BUTTON_COLOR,
            command=partial(go_back, root, go_to_main_menu),
            justify="center",
            height=1,
            padx=0,
            pady=0,
            text=Lg.lang["MainMenuLabel"],
            ).pack(side="left", padx=[2,4])
  
  tk.Button(action_frame,
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
            text=Lg.lang["Exit"],
            ).pack(side="left", padx=[4,2])
  
  root.mainloop()
