# Any number above 0 is refered to the number of mines in proximity
BOARDVALUESGUIDE = {
  0: "blankSpace",
  -1: "broccoli",
  -2: "nullSpace",
}

# Each tile in the tilesBoard matrix has a checked and tileValue value
#   checked defines if the specific tile has been click before, is a null space or 
#     if it was revealed by clicking another empty tile in the proximity
#   tileValue is the current value of a checked tile, being empty for empty tiles, a nullspace 
#     or the number of broccolis in the proximity of the tile
#   flagged indicates if the current tile has been flagged by the player as a possible broccoli
BOARDTILEVALUE = {"checked": False, "tileValue": " ", "flagged": False}

# The available board shapes
# square: No changes
# cutCorners: Cut the corners of the board
# cross: Cut the board in a cross shape
# randomCutCorners: Cut the corners of the board, but every corner is randomized
BOARDSHAPES = ["square", "cutCorners", "cross", "randomCutcorners"]

# Indicates if the row or column of each corner starts from 0 or negative
# For corners on row 0 the increment is positive in row direction
#   same as corners on column 0
# For corners on last row or column, it is handled as an increment but from negative index up to 0 index (not include) 
#   In other words, a corner on last column starts from the far-left corner space and increments until it reaches the last column
#   for a 5x5 board with corner size 2 the indexes would be [-2] [-1], where [-1] is the last column and [-2] the previous one
# The -1 values are used to indicate this behaviour while the 0 values indicate normal increments
CORNERGUIDE = [[0,0], [0,-1], [-1,0], [-1,-1]]

# Board sizes types
BOARDSIZES = ["Small", "Medium", "Big"]

# The sizes [min, max] for each board size type
# The min and max applies for both number of rows and columns
BOARDSIZEVALUES = {
  "Small": [4, 10],
  "Medium": [11, 20],
  "Big": [21, 30]
  }

# The maximun percent the board can use from the total screen height
BOARDMAXIMUNSIZEPERCENT = 70

# Pixel size of a tile in the board (measured by "hand")
TILEPIXELSIZE = 24