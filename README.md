# N-Queen-s-Problem
For CISC 352: Artificial Intelligence (W2020)
In Python 3


## Iterative Repair
Initializes the board by putting n queens on the diagonal. Moves the queen with the most queens attacking it to the safest position in the same column (to the position with the least amount of queens attacking it). If it gets stuck at a local optimum, it scraps the board and generates a new board with each queen placed on a random unique row in its own column. Then it repeats the process

#### Useful links: 
* https://github.com/ichko/ai/tree/master/03_n_queens
* https://en.wikipedia.org/wiki/Min-conflicts_algorithm
* https://github.com/kushjain/Min-Conflicts
