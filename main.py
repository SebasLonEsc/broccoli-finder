from src.logic.board import BoardGenerator

def main():
  rows = int(input("Enter the rows:"))
  columns = int(input("Enter the columns:"))
  broccoliAmount = int(input("Enter the number of broccolis:"))
  board = BoardGenerator(rows,columns,broccoliAmount)
  print(board["board"])

main()