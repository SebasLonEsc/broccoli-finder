from src.logic.board import BoardGenerator

def main():
  rows = int(input("Enter the rows:"))
  columns = int(input("Enter the columns:"))
  board = BoardGenerator(rows,columns)
  print(board)

main()