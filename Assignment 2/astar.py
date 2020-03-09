import os
from heapq import *
from copy import copy, deepcopy

class Position:
    def __init__ (self, x,y, came_from=None, cost_so_far=float('inf')):
        self.x=x
        self.y=y
        self.came_from = came_from
        self.cost_so_far = cost_so_far
        
    def __lt__(self, other): #breaks ties in the priority queue, doesn't matter which comes first
        return True

class Maze: #Creates a Maze which is stored as a 2D Array
    def __init__(self, maze):
        self.maze=maze
        self.start=self.find('S')
        self.end=self.find('G')

    def chebyshev(self, a, b):#Returns the Chebyshev Distance of A Maze for diagonal
        return max(abs(b.x-a.x),abs(b.y-a.y))

    def manhattan(self, a, b):#Returns the Manhatten Distance of A Maze for non-diagonal
        return abs(a.x - b.x) + abs(a.y - b.y)

    def find(self, point):#Finds the specific string in the maze
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):#The Number of Columns is not always the same as the number of rows, maze is either rectangular or square
                if self.maze[row][col]==point:
                    return Position(col,row)

    def diagNeighbours(self, pos):
        """
            Finds the diagonal neighbours of the point.
        """
        neigh = []
        maze = self.maze
        x = pos.x
        y = pos.y
        if x>0 and y>0 and maze[y-1][x-1] != 'X': #Checks the Upper Left Position
            neigh.append(Position(x-1, y-1, came_from=pos))
            
        if x>0 and y<len(maze)-1 and maze[y+1][x-1] != 'X': #Checks the Lower Left Position
            neigh.append(Position(x-1, y+1, came_from=pos))
            
        if x<len(maze[0])-1 and y>0 and maze[y-1][x+1] != 'X': #Checks the Upper Right Position
            neigh.append(Position(x+1, y-1, came_from=pos))
            
        if x<len(maze[0])-1 and y<len(maze)-1 and maze[y+1][x+1] != 'X': #Checks the Lower Right Position
            neigh.append(Position(x+1, y+1, came_from=pos))
        return neigh
    
    def neighbours(self,pos):#Finds the Horizontal and Vertical Neighbours of a certain position in the maze
        neigh=[]
        x=pos.x
        y=pos.y
        maze=self.maze
        if x>0 and maze[y][x-1]!= 'X':#Checks Left Position
            neigh.append(Position(x-1,y, came_from=pos))
        if len(maze[0])-1 and maze[y][x+1] != 'X':#Checks Right Position
            neigh.append(Position(x+1, y, came_from=pos))
        if y > 0 and maze[y-1][x] != 'X':#Checks the Upper Position
            neigh.append(Position(x, y-1, came_from=pos))
        if y < len(maze)-1 and maze[y+1][x] != 'X':#Checks the Lower Position
            neigh.append(Position(x, y+1, came_from=pos))
        return neigh

    def astarDiag(self):
        '''
        Seems to be okay, but pathing seems to be illogical sometimes
        '''
        frontier = []
        start = self.start
        start.cost_so_far = 0
        end = self.end
        heappush(frontier, (0, start))

        while not len(frontier)==0: #while frontier isn't empty 
            current = heappop(frontier)[1]
            x = current.x
            y = current.y
            if self.maze[y][x] == 'G':
                break
            neighbours = self.neighbours(current)+ (self.diagNeighbours(current))
            for nex in neighbours:
                new_cost = current.cost_so_far + 1
                if new_cost < nex.cost_so_far:
                    nex.cost_so_far = new_cost
                    priority = new_cost + self.chebyshev(end, nex)
                    heappush(frontier, (priority, nex))
                    nex.came_from = current
        #Solution has been found, move from Goal to Start, placing the path down as we go
        solution = deepcopy(self.maze)
        current = current.came_from
        while current.came_from != None:
            solution[current.y][current.x] = 'P'
            current = current.came_from
        return solution

    def astar(self):#finds he most optimal path, such that an agent cannot move diagonally on a maze
        frontier = []
        start = self.start
        start.cost_so_far = 0
        end = self.end
        heappush(frontier, (0, start))

        while not len(frontier)==0: #while frontier isn't empty 
            current = heappop(frontier)[1]
            x = current.x
            y = current.y
            if self.maze[y][x] == 'G':
                break
            neighbours = self.neighbours(current)
            for nex in neighbours:
                new_cost = current.cost_so_far + 1
                if new_cost < nex.cost_so_far:
                    nex.cost_so_far = new_cost
                    priority = new_cost + self.manhattan(end, nex)
                    heappush(frontier, (priority, nex))
                    nex.came_from = current
                    
        #Solution has been found, move from Goal to Start, placing the path down as we go
        solution = deepcopy(self.maze)
        current = current.came_from
        while current.came_from != None:
            solution[current.y][current.x] = 'P'
            current = current.came_from
        return solution
def readFile(filename):
    boards=[]
    with open(filename) as f:
        file=f.readlines()
    board=[]
    for row in file:
        if row== '\n':#multiple boards were found in the file
            boards.append(board)
            board=[]
        else:
            board.append(list(row.rstrip('\n')))
    boards.append(board)
    return boards

def writeOutput(solutions,filename):#writes the solutions to a text file
    with open(filename,'w') as out:
        for ind in range(len(solutions)):
            out.write('A*\n')
            for row in solutions[ind]:
                line = ''.join(row)+"\n"
                out.write(line)
            out.write("\n")

def solveXY():
    mazes=readFile('pathfinding_a.txt')
    sol=[]
    for g in mazes:
        grid=Maze(g)
        sol.append(grid.astar())
    writeOutput(sol, 'pathfinding_a_out.txt')
def solveDiag():
    mazes = readFile('pathfinding_b.txt')
    sol = []
    for g in mazes:
        grid = Maze(g)
        sol.append(grid.astarDiag())
    writeOutput(sol, 'pathfinding_b_out.txt')                                                           

solveXY()
solveDiag()
