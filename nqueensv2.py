import random
import time
from datetime import timedelta

#An Object Oriented Approach to the NQueens Problem
#CISC 352, Queen's University Winter 2020

class nQueens:

    #Initialize the board

    def __init__(self, size,debug=False):
        self.board=[None]*size
        self.rowConf=[0]*size#determines how many conflicts are in a certain row
        self.lDiagConf=[0]*(2*size-1) #determines how many conflicts are in a specific left diagonal
        self.rDiagConf=[0]*(2*size-1) #determines how many conflicts are in a specific right diagonal
        self.confRemain=0 #total amount of conflicts remaining
        self.iterations=100
        self.resets=0
        self.repairs=0
        self.debug=debug
        self.start(size)
        self.solve(size)
        if self.debug: self.showFullBoard(size)


    def showFullBoard(self, size):
        """Show the full NxN board"""
        for row in range(self.size):
            line = ""
            for column in range(self.size):
                if self.positions[column] == row:
                    line += "Q "
                else:
                    line+=". "
            print(line)

    def start(self, size):
        self.board=[None]*size
        for col in range(size):
            row=self.minConf(col, size)
            self.createQueen(row, col,size)

    def solve(self, size):
        success=False
        for i in range(self.iterations):
            col=self.conflictCol(size)
            if col<0:
                success=True
                self.repairs+=i
                break
            row=self.minConf(col,size)
            #if self.debug: print("Queen "+str(col)+" from row " +str(self.board[col]) + " to row " + str(row)+".")
            self.delQueen(self.board[col],col,size)
            self.createQueen(row, col,size)
        if not success:
            self.repairs+=self.iterations
            self.reset(size)

    def posConflict(self, row, col, size):#returns how many current queen's can reach the given position
        return self.rowConf[row]+self.lDiagConf[(size-1)+(col-row)]+self.rDiagConf[col+row]

    def conflictCol(self,size):
        colConf=[]
        numConf=0
        for col in range(0, size):
            row=self.board[col]
            numConf=self.posConflict(row,col,size)
            if numConf!=3:#Three means 0 violations, meaning only one queen can reach that pos, the one that is currenlty on that pos
                colConf.append(col)
        if len(colConf)==0:
            return -1
        return random.choice(colConf)
    
    def delQueen(self, row, col,size):#Delete's a queen's position data, updating the board and removing any conflicts the queen had
        self.board[col]=None
        self.rowConf[row]-=1
        self.lDiagConf[(size-1)+(col-row)]-=1
        self.rDiagConf[row+col]-=1
    
    def createQueen(self, row, col,size):#update the board to show the new position of a queen
        self.board[col]=row
        self.rowConf[row]+=1
        self.lDiagConf[(size-1)+(col-row)]+=1
        self.rDiagConf[row+col]+=1

    def reset(self, size):
        self.board=[None]*size
        self.rowConf=[0]*size#determines how many conflicts are in a certain row
        self.lDiagConf=[0]*(2*size-1) #determines how many conflicts are in a specific left diagonal
        self.rDiagConf=[0]*(2*size-1) #determines how many conflicts are in a specific right diagonal
        self.confRemain=0 #total amount of conflicts remaining
        self.resets+=1
        self.start(size)
        self.solve(size)

    def minConf(self, col, size):
        minn=float('inf')
        cand=[]
        for row in range(size):
            rowConf=self.posConflict(row,col,size)
            if rowConf<minn:
                minn=rowConf
                cand=[row]
            elif rowConf==minn:
                cand.append(row)
        choice=random.choice(cand)#pick one of the best possible rows randomly
        return choice

                                                
    def showFullBoard(self, size):
        """Show the full NxN board"""
        for row in range(size):
            line = ""
            for col in range(size):
                if self.board[col] == row:
                    line += "Q "
                else:
                    line+=". "
            print(line)

        
    
def main():
    input = open("nqueens.txt")
    output = open("nqueens_out.txt", "w")
    lines = input.readlines()
    lines = [x.strip() for x in lines]
    lines = [int(i) for i in lines]
    for size in lines:
        print("Board size:\t\t"+str(size))
        start=time.time()
        board = nQueens(size)
        
        timeTaken=time.time()-start
        print("Solution Found in:\t\t"+str(timedelta(seconds=timeTaken)))
        #print("Remaining Conflicts: "+str(board.confRemain))
        solution=[]
        for row in board.board:
            solution.append(row+1)
        #print(solution)#prints what will be written to the text file
        print("Required # of Resets: "+str(board.resets))
        print("Required # of Repairs: "+str(board.repairs))
        print("---")
               
        output.write(str(solution) + "\n")

main()
        
        
