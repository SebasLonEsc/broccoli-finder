#Any number above 0 is refered to the number of mines in proximity
boardValuesGuide = {
  0: "blankSpace",
  -1: "broccoli",
  -2: "nullSpace",
}

boardTileValue = {"checked": False, "tileValue": " "}

# The available board shapes
# square: No changes
# cutCorners: Cut the corners of the board
# cross: Cut the board in a cross shape
# randomCutCorners: Cut the corners of the board, but every corner is randomized
boardShapes = ["square","cutCorners","cross","randomCutcorners"]

# Indicates if the row or column of each corner starts from 0 or negative
# For corners on row 0 the increment is positive in row direction
#   same as corners on column 0
# For corners on last row or column, it is handled as an increment but from negative index up to 0 index (not include) 
#   In other words, a corner on last column starts from the far-left corner space and increments until it reaches the last column
#   for a 5x5 board with corner size 2 the indexes would be [-2] [-1], where [-1] is the last column and [-2] the previous one
# The -1 values are used to indicate this behaviour while the 0 values indicate normal increments
cornerGuide = [[0,0], [0,-1], [-1,0], [-1,-1]]