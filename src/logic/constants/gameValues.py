import random

import src.lang.language as Lg

def get_endgame_text(texts):
  """ Returns a random text from a list of strings

  Args:
    texts (array[str]): An array of strings
  
  Returns:
    str: A random string from the texts argument
  """
  text_position = random.randint(0, len(texts)-1)
  return texts[text_position]

def get_winning_text():
  """Returns the text upon winning the game

  Returns:
    str: The congratulations text
  """
  if len(Lg.lang["Winning_Texts"]) == 1:
    return Lg.lang["Winning_Texts"][0]

  return get_endgame_text(Lg.lang["Winning_Texts"])

def get_losing_text():
  """Returns the text upon losing the game

  Returns:
    str: The losing text
  """
  if len(Lg.lang["Losing_Texts"]) == 1:
    return Lg.lang["Losing_Texts"][0]

  return get_endgame_text(Lg.lang["Losing_Texts"])

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

RAINBOW_BROCCOLI_PROPORTION_CHANCES = [[0.1, 0.2], [0.2, 0.25], [0.25, 0.3]]

RAINBOW_BROCCOLI_PERCENT = [0.25, 0.33, 0.5]