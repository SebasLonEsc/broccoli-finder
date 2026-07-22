# Display text when winning the game
WINNINGTEXT = "CONGRATULATIONS\nYou Won the Game!!"

# Display text when losing the game
LOSINGTEXT = "Sorry you lost"

# Game Difficulties types
GAMEDIFFICULTIES = ["Easy", "Normal", "Hard"]

# The maximun amount of broccolis per game difficulty
# The total is found using the total amount of tiles in the board
GAMEBROCCOLIPERCENTS = {
  "Easy": [0.05, 0.1],
  "Normal": [0.12, 0.2],
  "Hard": [0.22, 0.3]
  }