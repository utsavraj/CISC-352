import random
import os
import time

#Generates a random n x n board
def random_board(nr):
  board = list(range(nr))
  random.shuffle(board)
  return board


def nqueens(nr):
  return min_conflicts(random_board(nr), nr)
  
# Creates The Solution
# Example of a board generated eg. (2, 4, 1 , 3)
# - Q - -
# - - - Q
# Q - - -
# - - Q -
# nr - size of the board
# soln - solution index (needs to be incremented by one)
# number of iterations before the system is stopped due to local minima

def min_conflicts(soln, nr, iters=1000):
  def random_pos(li, filt):
    return random.choice([i for i in range(nr) if filt(li[i])])

  for k in range(iters):
    conflicts = find_conflicts(soln, nr)
    #If conflicts are zero, it means we are at the goal state
    if sum(conflicts) == 0:
      #Index of row starts from 1
      soln = [x+1 for x in soln]
      return soln
    
    #Choose a random column  
    col = random_pos(conflicts, lambda elt: elt > 0)
    vconfs = [hits(soln, nr, col, row) for row in range(nr)]
    soln[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))
  raise Exception("Try more iterations.")



# Returns the number of hits for queen in each column as a list
def find_conflicts(soln, nr):
  x = [hits(soln, nr, col, soln[col]) for col in range(nr)]
  return x

#Checks for number of queens attacking the queen in the given column
# col - index of column of the queen
# row - index of the queen's row
def hits(soln, nr, col, row):
  conflict = 0
  for i in range(nr):
    if i == col:
      continue
    # If the queens are in the same row/ digonal to each other 
    # increment conflict by 1
    if soln[i] == row or abs(i - col) == abs(soln[i] - row):
      conflict += 1
  return conflict



#Function that writes the answer to the output file
def nqueens_sol(queens, nqueens_out):
  #-----#
  start_time = time.time()
  #-----#

  nqueens_out.write(str(nqueens(int(queens))))
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
