import unittest
import numpy as np
import tkinter as tk
from unittest.mock import patch

import src.lang.language as Lg
import src.view.boardInterface as boardInterface
from src.logic.board import Board, board_generator
from src.logic.constants.gameValues import GAME_OVER_LANG_CODE
from src.logic.constants.boardValues import GET_BOARD_VALUE, BOARD_SIZE_VALUES
from src.logic.constants.styleValues import TILE_BACKGROUND_COLOR, PROXIMITY_COLORS

class TestChangeFlagStatus(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    self.button = tk.Button(self.root)
    self.button.pack()

  def test_change_flag_status(self):
    with (patch.object(tk, "PhotoImage") as image,
          patch.object(tk.Button, "config")):
      image.return_value = None

      expected_flag_status = not boardInterface.flag_command
      boardInterface.change_flag_status(self.button)

      self.assertEqual(expected_flag_status,
                       boardInterface.flag_command,
                       "Incorrect flag status")

  def tearDown(self):
    self.root.destroy()

class TestHandleFlagTile(unittest.TestCase):
  def setUp(self):
    boardInterface.broccoli_counter_value = 1
    self.root = tk.Tk()
    self.broccoli_counter = tk.Label(self.root)
    self.broccoli_counter.pack()

    size = 2
    self.board_object = Board(size, size)
    self.buttons = np.empty(shape=[size, size], dtype="object")
    for row in range(0, size):
      for column in range(0, size):
        button = tk.Button(self.root)
        button.pack()
        self.buttons[row, column] = button

    self.checked_position = [0,1]
    tiles_board = self.board_object.tiles_board
    tile = tiles_board[self.checked_position[0],
                       self.checked_position[1]]
    tile["checked"] = True
    tiles_board[self.checked_position[0],
                self.checked_position[1]] = tile
    self.board_object.change_tiles_board(tiles_board)

  def test_handle_flag_tile_checked(self):
    return_value = boardInterface.handle_flag_tile(self.board_object,
                                                   self.buttons,
                                                   self.checked_position,
                                                   self.broccoli_counter)

    self.assertEqual(None,
                     return_value,
                     "Returned value should be None")

  def test_handle_flag_tile(self):
    with (patch.object(tk, "PhotoImage") as image,
          patch.object(tk.Button, "config"),
          patch.object(tk.Label, "config")):
      image.return_value = None
      move_position = [0,0]

      expected_counter = boardInterface.broccoli_counter_value - 1
      return_value = boardInterface.handle_flag_tile(self.board_object,
                                                     self.buttons,
                                                     move_position,
                                                     self.broccoli_counter)

      self.assertTrue(return_value, "New flag status should be True")
      self.assertEqual(expected_counter,
                       boardInterface.broccoli_counter_value,
                       "Broccoli counter value should have been reduced by 1")

      expected_counter = boardInterface.broccoli_counter_value + 1
      return_value = boardInterface.handle_flag_tile(self.board_object,
                                                      self.buttons,
                                                      move_position,
                                                      self.broccoli_counter)

      self.assertFalse(return_value, "New flag status should be False")
      self.assertEqual(expected_counter,
                       boardInterface.broccoli_counter_value,
                       "Broccoli counter value should have been increase by 1")

  def tearDown(self):
    self.root.destroy()

class TestHandleRevealBroccolis(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()

    size = 3
    self.board_object = board_generator(size, size, 3)
    self.buttons = np.empty(shape=[size, size], dtype="object")
    self.button_text = "Broccoli"
    for row in range(0, size):
      for column in range(0, size):
        button = tk.Button(self.root, text=self.button_text)
        button.pack()
        self.buttons[row, column] = button

    tiles_board = self.board_object.tiles_board
    rainbow_broccoli_pos = self.board_object.broccoli_positions[1]    
    rainbow_broccoli_tile = tiles_board[rainbow_broccoli_pos[0],
                                        rainbow_broccoli_pos[1]]
    rainbow_broccoli_tile["tileValue"] = GET_BOARD_VALUE["rainbowBroccoli"]

    flowering_broccoli_pos = self.board_object.broccoli_positions[2]
    flowering_broccoli_tile = tiles_board[flowering_broccoli_pos[0],
                                          flowering_broccoli_pos[1]]
    flowering_broccoli_tile["tileValue"] = GET_BOARD_VALUE["floweringBroccoli"]

  def test_handle_reveal_broccolis(self):
    with (patch("src.view.boardInterface.open_pillow_image") as image,
          ):
      image.return_value = None

      move_position = self.board_object.broccoli_positions[0]
      boardInterface.handle_reveal_broccolis(self.board_object,
                                             self.buttons,
                                             move_position)

      broccoli_positions = self.board_object.broccoli_positions
      for pos in broccoli_positions:
        new_text = self.buttons[pos[0], pos[1]].cget("text")
        self.assertNotEqual(self.button_text,
                            new_text,
                            "Button text should have changed")

  def tearDown(self):
    self.root.destroy()

class TestHandleGameStatus(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
    
    self.size = 3
    self.board_object = board_generator(self.size, self.size, 3)
    self.buttons = np.empty(shape=[self.size, self.size], dtype="object")
    self.button_func = lambda: True
    for row in range(0, self.size):
      for column in range(0, self.size):
        button = tk.Button(self.root, command=self.button_func)
        button.pack()
        self.buttons[row, column] = button

  def test_handle_game_status(self):
    with patch("src.view.boardInterface.handle_reveal_broccolis") as mocked_func:
      move_pos = [0,0]
      boardInterface.handle_game_status(self.board_object,
                                        self.buttons,
                                        move_pos,
                                        True)

      mocked_func.assert_called_once()

      for row in range(0, self.size):
        for column in range(0, self.size):
          button = self.buttons[row, column]

          self.assertNotEqual(button.invoke(),
                              self.button_func(),
                              "Button command should have changed")

  def tearDown(self):
    self.root.destroy()

class TestCreateProximityTileImages(unittest.TestCase):
  def mocked_func(_, path, __, ___):
    return path

  def test_create_proximity_tile_images(self):
    with patch.object(boardInterface, "open_pillow_image", new_callable=lambda: self.mocked_func):
      images_array = ["first", "second", "third"]
      tile_images = boardInterface.create_proximity_tile_images(images_array)

      for i in range(len(images_array)):
        path = images_array[i]
        returned_value = str(tile_images[i])
        self.assertTrue(path in returned_value,
                        "Incorrect tile images array")

class TestHandleRevealedTiles(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()
        
    self.size = 3
    self.board_object = board_generator(self.size, self.size, 3)
    self.buttons = np.empty(shape=[self.size, self.size], dtype="object")
    self.button_func = lambda: False
    self.button_text = "Tile"
    for row in range(0, self.size):
      for column in range(0, self.size):
        button = tk.Button(self.root,
                           text=self.button_text,
                           command=self.button_func,
                           bg=TILE_BACKGROUND_COLOR)
        if(row == 0 and column == 0):
          button.config(bg=PROXIMITY_COLORS[0])

        button.pack()
        self.buttons[row, column] = button

    tiles_board = self.board_object.tiles_board
    self.normal_proximity_tile_pos = [0,1]
    normal_proximity_tile = tiles_board[self.normal_proximity_tile_pos[0],
                                        self.normal_proximity_tile_pos[1]]
    normal_proximity_tile["tileValue"] = 5 # Normal proximity number
    normal_proximity_tile["checked"] = True
    tiles_board[self.normal_proximity_tile_pos[0],
                self.normal_proximity_tile_pos[1]] = normal_proximity_tile

    self.rainbow_proximity_tile_pos = [0,2]
    rainbow_proximity_tile = tiles_board[self.rainbow_proximity_tile_pos[0],
                                         self.rainbow_proximity_tile_pos[1]]
    rainbow_proximity_tile["tileValue"] = 15 # Rainbow proximity number
    rainbow_proximity_tile["checked"] = True
    tiles_board[self.rainbow_proximity_tile_pos[0],
                self.rainbow_proximity_tile_pos[1]] = rainbow_proximity_tile

    self.board_object.change_tiles_board(tiles_board)

  def test_handle_revealed_tiles(self):
    with patch("src.view.boardInterface.create_proximity_tile_images") as mocked_func:
      mocked_func.return_value = [None] * 9 # 9 proximity numbers including 0
      boardInterface.handle_revealed_tiles(self.board_object, self.buttons)

      normal_proximity_button = self.buttons[self.normal_proximity_tile_pos[0],
                                             self.normal_proximity_tile_pos[1]]
      rainbow_proximity_button = self.buttons[self.rainbow_proximity_tile_pos[0],
                                              self.rainbow_proximity_tile_pos[1]]

      self.assertNotEqual(normal_proximity_button["text"],
                          self.button_text,
                          "Button text should've changed")
      self.assertNotEqual(rainbow_proximity_button["text"],
                          self.button_text,
                          "Button text should've changed")

      self.assertNotEqual(normal_proximity_button.invoke(),
                          self.button_func(),
                          "Button command should've changed")
      self.assertNotEqual(rainbow_proximity_button.invoke(),
                          self.button_func(),
                          "Button command should've changed")

  def tearDown(self):
    self.root.destroy()

class TestHandleRainbowBroccoliReveal(unittest.TestCase):
  def setUp(self):
    boardInterface.broccoli_counter_value = 3
    self.root = tk.Tk()
    self.broccoli_counter = tk.Label(self.root)
    self.broccoli_counter.pack()

    size = 3
    self.empty_board_object = Board(size, size)
    self.board_object = board_generator(size, size, 3)
    self.buttons = np.empty(shape=[size, size], dtype="object")
    self.button_func = lambda: False
    self.button_text = "Tile"

    for row in range(0, size):
      for column in range(0, size):
        button = tk.Button(self.root,
                           text=self.button_text,
                           command=self.button_func)
        button.pack()
        self.buttons[row, column] = button
    checked_flowering_button_pos = self.board_object.broccoli_positions[1]
    checked_flowering_button = self.buttons[checked_flowering_button_pos[0],
                                            checked_flowering_button_pos[1]]
    checked_flowering_button.config(bg=PROXIMITY_COLORS[0])
    self.buttons[checked_flowering_button_pos[0],
                 checked_flowering_button_pos[1]] = checked_flowering_button

    self.flowering_broccoli_pos = self.board_object.broccoli_positions[2]
    board = self.board_object.board
    board[checked_flowering_button_pos[0],
          checked_flowering_button_pos[1]] = GET_BOARD_VALUE["floweringBroccoli"]
    board[self.flowering_broccoli_pos[0],
          self.flowering_broccoli_pos[1]] = GET_BOARD_VALUE["floweringBroccoli"]
    self.board_object.change_board(board)

    tiles_board = self.board_object.tiles_board    
    flowering_broccoli_tile = tiles_board[self.flowering_broccoli_pos[0],
                                        self.flowering_broccoli_pos[1]]
    flowering_broccoli_tile["tileValue"] = GET_BOARD_VALUE["rainbowBroccoli"]
    flowering_broccoli_tile["flagged"] = True
    tiles_board[self.flowering_broccoli_pos[0],
                self.flowering_broccoli_pos[1]] = flowering_broccoli_tile
    self.board_object.change_tiles_board(tiles_board)

  def test_handle_rainbow_broccoli_reveal(self):
    with patch.object(tk, "PhotoImage") as image:
      image.return_value = None
      expected_counter_value = boardInterface.broccoli_counter_value - 1
      move_position = self.board_object.broccoli_positions[0]
      boardInterface.handle_rainbow_broccoli_reveal(self.board_object,
                                                    self.buttons,
                                                    move_position,
                                                    self.broccoli_counter)

      rainbow_broccoli_button = self.buttons[move_position[0],
                                             move_position[1]]
      self.assertNotEqual(rainbow_broccoli_button["text"],
                          self.button_text,
                          "Button text should've changed")
      self.assertNotEqual(rainbow_broccoli_button.invoke(),
                          self.button_func(),
                          "Button command should've changed")

      flowering_broccoli_button = self.buttons[self.flowering_broccoli_pos[0],
                                               self.flowering_broccoli_pos[1]]
      self.assertNotEqual(flowering_broccoli_button["text"],
                          self.button_text,
                          "Button text should've changed")
      self.assertNotEqual(flowering_broccoli_button.invoke(),
                          self.button_func(),
                          "Button command should've changed")

      self.assertEqual(expected_counter_value,
                       boardInterface.broccoli_counter_value,
                       "Broccoli counter should've changed")

  def test_handle_rainbow_broccoli_reveal_no_flowering(self):
    with patch.object(tk, "PhotoImage") as image:
      image.return_value = None
      move_position = self.board_object.broccoli_positions[0]
      return_value = boardInterface.handle_rainbow_broccoli_reveal(self.empty_board_object,
                                                                   self.buttons,
                                                                   move_position,
                                                                   self.broccoli_counter)

      self.assertFalse(return_value, "Returned value should be False")

  def tearDown(self):
    self.root.destroy()

class TestHandleClick(unittest.TestCase):
  def setUp(self):
    boardInterface.flag_command = True
    self.root = tk.Tk()
    self.broccoli_counter = tk.Label(self.root)
    self.broccoli_counter.pack()
    self.win_label = tk.Label(self.root)
    self.win_label.pack()

    size = 3
    self.buttons = np.empty(shape=[size, size], dtype="object")
    for row in range(0, size):
      for column in range(0, size):
        button = tk.Button(self.root)
        button.pack()
        self.buttons[row, column] = button

    broccoli_value = GET_BOARD_VALUE["broccoli"]
    rainbow_broccoli = GET_BOARD_VALUE["rainbowBroccoli"]
    empty_tile = 0
    proximity_tile = 1
    self.board_object = Board(size, size)
    board = [[empty_tile, proximity_tile, broccoli_value],
             [empty_tile, proximity_tile, rainbow_broccoli],
             [empty_tile, proximity_tile, broccoli_value]]
    self.board_object.change_board(np.array(board))
    self.board_object.add_broccoli_positions([0,2])
    self.rainbow_broccoli_pos = [1,2]
    self.board_object.add_broccoli_positions(self.rainbow_broccoli_pos)
    self.board_object.add_broccoli_positions([2,2])

  def test_handle_click_flag_command(self):
    with patch("src.view.boardInterface.handle_flag_tile") as mocked_handle_flag:
      boardInterface.handle_click(self.board_object,
                                  self.buttons,
                                  [0,0],
                                  self.win_label,
                                  self.broccoli_counter)

      mocked_handle_flag.assert_called_once()

  def test_handle_click_rainbow_broccoli(self):
    boardInterface.flag_command = False
    with (patch("src.view.boardInterface.handle_revealed_tiles") as mocked_handle_revealed_tiles,
          patch("src.view.boardInterface.handle_rainbow_broccoli_reveal") as mocked_handle_rainbow_broccoli_reveal):
      boardInterface.handle_click(self.board_object,
                                  self.buttons,
                                  self.rainbow_broccoli_pos,
                                  self.win_label,
                                  self.broccoli_counter)

      mocked_handle_rainbow_broccoli_reveal.assert_called_once()
      mocked_handle_revealed_tiles.assert_called_once()

  def test_handle_click_game_over(self):
    boardInterface.flag_command = False
    with (patch("src.view.boardInterface.handle_revealed_tiles") as mocked_handle_revealed_tiles,
          patch("src.view.boardInterface.handle_game_status") as mocked_handle_game_status):
      broccoli_positions = self.board_object.broccoli_positions
      broccoli_pos = broccoli_positions[0]
      for pos in broccoli_positions:
        if self.board_object.board[pos[0], pos[1]] == GET_BOARD_VALUE["broccoli"]:
          broccoli_pos = pos
          break

      boardInterface.handle_click(self.board_object,
                                  self.buttons,
                                  broccoli_pos,
                                  self.win_label,
                                  self.broccoli_counter)
      
      mocked_handle_revealed_tiles.assert_called_once()
      mocked_handle_game_status.assert_called_once()

      game_over_texts = Lg.lang[GAME_OVER_LANG_CODE]
      win_label_text = self.win_label["text"]
      is_game_over_text = win_label_text in game_over_texts
      self.assertTrue(is_game_over_text,
                      "Label should've change to a game over text")

  def tearDown(self):
    self.root.destroy()

class TestCreateBoardCanvas(unittest.TestCase):
  def setUp(self):
    self.root = tk.Tk()

  def test_create_board_canvas(self):
    with (patch.object(tk, "Canvas") as mocked_canvas,
          patch.object(tk, "Scrollbar") as mocked_scroll_bar):
      frame = boardInterface.create_board_canvas(self.root)

      self.assertTrue(frame.winfo_exists(),
                      "The canvas frame should exists")
      mocked_canvas.assert_called_once()
      mocked_scroll_bar.assert_called_once()

  def tearDown(self):
      self.root.destroy()

class TestCreateBoardInterface(unittest.TestCase):
  def setUp(self):
    self.board_object = board_generator(3,3,3)
    big_size = BOARD_SIZE_VALUES["Big"][1]
    self.canvas_board_object = board_generator(big_size, big_size, 2)
    self.go_back_func = lambda: None

  def test_create_board_interface(self):
    with (patch("src.view.boardInterface.create_menu") as create_menu_mock,
          patch.object(tk, "PhotoImage") as photo_image_mock,
          patch.object(tk.Tk, "mainloop") as main_loop_mock):
      photo_image_mock.return_value = None

      root = boardInterface.create_board_interface(self.board_object,
                                                   self.go_back_func,
                                                   self.go_back_func)

      create_menu_mock.assert_called_once()
      main_loop_mock.assert_called_once()

      self.assertTrue(root.winfo_exists(), "Root should exists")
      root.destroy()

  def create_board_canvas_mock(_, root):
    return tk.Frame(root)

  def test_create_board_interface_canvas_board(self):
    with (patch("src.view.boardInterface.create_menu") as create_menu_mock,
          patch.object(boardInterface, "create_board_canvas", new_callable=lambda: self.create_board_canvas_mock),
          patch.object(tk, "PhotoImage") as photo_image_mock,
          patch.object(tk.Tk, "mainloop") as main_loop_mock):
      photo_image_mock.return_value = None

      root = boardInterface.create_board_interface(self.canvas_board_object,
                                                   self.go_back_func,
                                                   self.go_back_func)

      create_menu_mock.assert_called_once()
      main_loop_mock.assert_called_once()

      self.assertTrue(root.winfo_exists(), "Root should exists")
      root.destroy()