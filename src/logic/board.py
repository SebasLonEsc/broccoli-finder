import numpy as np

def BoardGenerator(rows, columns):
  board = np.zeros(shape=[rows,columns],dtype=np.int8)
  return board