import os

####### NEEDS TO BE DONE #######
#iterative repair method using 
#the minimum conflicts algorithm

def minimum_conflicts_algo(queens):
  #Currently we create an array of sol with length of line in input and values from 1 to line
  sol = [1] * int(queens)
  for i in range(int(queens)):
    sol[i] = (i+1)
  return str(sol)


#Function that writes the answer to the output file
def nqueens_sol(queens, nqueens_out):
  nqueens_out.write(minimum_conflicts_algo(queens))
  nqueens_out.write("\n")





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
