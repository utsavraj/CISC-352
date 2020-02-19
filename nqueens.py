import random
import os
import time

def nqueens(nr):
  return show(min_conflicts(list(range(nr)), nr), nr)

def show(soln, nr):
  solution = [0]*nr
  for i in range(nr):
    for col in range(nr):
      if soln[col] == nr - 1 - i:
        solution[col] = nr - i
  return solution

def min_conflicts(soln, nr, iters=1000):
  def random_pos(li, filt):
    return random.choice([i for i in range(nr) if filt(li[i])])

  for k in range(iters):
    confs = find_conflicts(soln, nr)
    if sum(confs) == 0:
      return soln
    col = random_pos(confs, lambda elt: elt > 0)
    vconfs = [hits(soln, nr, col, row) for row in range(nr)]
    soln[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))
  raise Exception("Try more iterations.")

def find_conflicts(soln, nr):
  return [hits(soln, nr, col, soln[col]) for col in range(nr)]

def hits(soln, nr, col, row):
  total = 0
  for i in range(nr):
    if i == col:
      continue
    if soln[i] == row or abs(i - col) == abs(soln[i] - row):
      total += 1
  return total



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
