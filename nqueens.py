#-///-RUNNING TIME-///-#
# n = 400: 151s
# n = 500: 232s
# n = 700:
#----------------------#

#!/usr/bin/env pypy
import random
import os
import time

# Generates a random n x n board
def random_board(nr):
  board = list(range(nr))
  random.shuffle(board)
  return board

# Trivial Solution for nr = 1 and no solution for nr = 2 or 3
def nqueens(nr):
  if (nr == 1):
    return [1]
  elif (nr == 2 or nr == 3 or nr < 1):
    return "No solution"
  else:
    return min_conflicts(random_board(nr), nr)
  
# Creates The Solution
# Example of a board generated eg. (2, 4, 1 , 3)
# - Q - -
# - - - Q
# Q - - -
# - - Q -
# nr - size of the board
# soln - solution index (needs to be incremented by one)
# iters = 1000. number of iterations after which a new random board is generated. 

def min_conflicts(soln, nr, iters=1000):
  def random_pos(li, filt):
    return random.choice([i for i in range(nr) if filt(li[i])])

  while(find_conflicts(soln, nr) != 0):
    for k in range(iters):
      conflicts = find_conflicts(soln, nr)
      #If conflicts are zero, it means we are at the goal state
      if sum(conflicts) == 0:
        #Index of row starts from 1
        soln = [x+1 for x in soln]
        return soln
      
      #Choose a random column  with conflict greater 0 as 
      #we do not want to disturb a queen in good position
      col = random_pos(conflicts, lambda elt: elt > 0)

      #For the given random col, calculate the number of hits for moving it in each row and return it as a list named vconfs.
      vconfs = [hits(soln, nr, col, row) for row in range(nr)]

      #For the random given column, choose the row position with least conflict - choose randomly if any tie.
      soln[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))

    # If stuck at a local minima after 1000 iterations, generate a new 
    # random board  
    soln = random_board(nr)


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
