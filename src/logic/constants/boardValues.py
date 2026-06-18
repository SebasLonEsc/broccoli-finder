#Any number above 0 is refered to the number of mines in proximity
boardValuesGuide = {
  0: "blankSpace",
  -1: "broccoli",
  -2: "nullSpace",
}

# The available board shapes
# square: No changes
# cutCorners: Cut the corners of the board
# cross: Cut the board in a cross shape
# randomCutCorners: Cut the corners of the board, but every corner is randomized
boardShapes = ["square","cutCorners","cross", "randomCutcorners"]