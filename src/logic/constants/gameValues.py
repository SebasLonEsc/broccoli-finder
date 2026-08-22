import random

import src.lang.language as Lg

def get_endgame_text(texts):
  """ Returns a random text from a list of strings

  Args:
    texts (array[str]): An array of strings
  
  Returns:
    str: A random string from the texts argument
  """
  text_position = random.randrange(0, len(texts))
  return texts[text_position]

def get_winning_text():
  """Returns the text upon winning the game

  Returns:
    str: The congratulations text
  """
  if len(Lg.lang["Winning_Texts"]) == 1:
    return Lg.lang["Winning_Texts"][0]

  return get_endgame_text(Lg.lang["Winning_Texts"])

def get_game_over_text():
  """Returns the text upon losing the game

  Returns:
    str: The game over text
  """
  if len(Lg.lang["Game_Over_Text"]) == 1:
    return Lg.lang["Game_Over_Text"][0]

  return get_endgame_text(Lg.lang["Game_Over_Text"])

# Game types represented as numbers
GAME_TYPES = {
  1: "Console",
  2: "UI"
}

# The current game status after a move is done
# -1 -> Indicates a game over.
# 0 -> Indicate the game is still on.
# 1 -> Indicates a won game
GAME_STATUS = {
  -1: "Game Over",
  0: "Play",
  1: "Win"
}

# Returns the numeric equivalent for the game status
GET_GAME_STATUS = {
  "Game Over": -1,
  "Play": 0,
  "Win": 1
}

# Game Difficulties types
GAME_DIFFICULTIES = [
  "Easy",
  "Normal",
  "Hard"
  ]

# The maximun amount of broccolis per game difficulty
# The total is found using the total amount of tiles in the board
GAME_BROCCOLI_PERCENTS = {
  "Small": {
    "Easy": [0.08, 0.13],
    "Normal": [0.15, 0.25],
    "Hard": [0.28, 0.35]
  },
  "Medium": {
    "Easy": [0.05, 0.1],
    "Normal": [0.12, 0.2],
    "Hard": [0.22, 0.3]
  },
  "Big": {
    "Easy": [0.05, 0.1],
    "Normal": [0.11, 0.15],
    "Hard": [0.18, 0.2]
  }
  }

# The chances to appear a rainbow broccoli based on the broccoli proportions
RAINBOW_BROCCOLI_PROPORTION_CHANCES = [[0.1, 0.2], [0.2, 0.25], [0.25, 0.35]]

# The probability of adding a rainbow broccoli for each proportion group
RAINBOW_BROCCOLI_CHANCE = [0.35, 0.45, 0.65]

# The minimun amount of broccolis needed to add a rainbow broccoli
MINIMUN_BROCCOLI_AMOUNT_FOR_RAINBOW_BROCCOLI = 4