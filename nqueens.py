import random
import time
import os

# Runs in O(n) time (Idea taken from: https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645)

def conflict(board):
  conflict = 0
  #frequency of queens in each row. Increments each time a queen is found in a row
  row_queen = [0]*(len(board) + 1)

  m_diagonal = [0]*(2*len(board)+ 1)

  s_diagonal = [0]*(2*len(board) + 1)

  for j in range(len(board)):
    val = board[j]
    row_queen[val] = row_queen[val] + 1
    m_diagonal[(val + j)] = m_diagonal[val + j] + 1
    s_diagonal[(len(board) - val + j)] = s_diagonal[(len(board) - val + j)] + 1 

  # For Queens in same row conflict, the queens make a complete graph - hence number of edges = queens attacking 

  for j in range(len(s_diagonal)):
    queens_row = 0
    m_diagonal_queens = 0
    s_diagonal_queens = 0

    if (j <= len(board)):
      queens_row = row_queen[j]
    
    m_diagonal_queens = m_diagonal[j]
    s_diagonal_queens = s_diagonal[j]

    conflict = conflict + ((queens_row * (queens_row - 1)) / 2) 
    conflict = conflict + ((m_diagonal_queens * (m_diagonal_queens - 1)) / 2) 
    conflict = conflict + ((s_diagonal_queens * (s_diagonal_queens - 1)) / 2) 

  return int(conflict)

def min_conflict(board, i):
  total_conflicts = [0]*len(board)
  temp_board = board
  for j in range(1, len(board)+ 1):
    temp_board[i] = j
    total_conflicts[j-1] = conflict(temp_board)
  return total_conflicts.index(min(total_conflicts))



#Creates a random board with no queens in same row, column
#Example of a board generated eg. (2, 4, 1 , 3)
# - Q - -
# - - - Q
# Q - - -
# - - Q -

def random_board(n):
  board = list(range(1,n+1))
  random.shuffle(board)
  return board

def iterative_repair(board):
  length = len(board)
  steps = 0
  while(conflict(board) != 0):
    for i in range(len(board)):
      board[i] = min_conflict(board, i) + 1
    steps = steps + 1

    if (steps > 10):
      board = random_board(length)
      steps = 0
  return board





#Function that writes the answer to the output file
def nqueens_sol(queens, nqueens_out):
  #-----#
  start_time = time.time()
  #-----#

  board = random_board(int(queens))
  nqueens_out.write(str(iterative_repair(board)))
  nqueens_out.write("\n")

  #-----#
  print("--- %s seconds ---" % (time.time() - start_time))
  #-----#

def main():
  #reads the input file
  f = open("nqueens.txt", "r")
  
  #deletes any pre-existing output file 
  #so answer is not appended to an existing file
  if os.path.exists("nqueens_out.txt"):
    os.remove("nqueens_out.txt")

  nqueens_out = open("nqueens_out.txt", "a")

  for line in f:
    nqueens_sol(line, nqueens_out)

  nqueens_out.close()
  f.close()



if __name__ == '__main__':
  main()
