from src.logic.board import boardGenerator

def main():
  rows = int(input("Enter the rows:"))
  columns = int(input("Enter the columns:"))
  broccoliAmount = int(input("Enter the number of broccolis:"))
  board = boardGenerator(rows, columns, broccoliAmount)

main()