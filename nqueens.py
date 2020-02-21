import random
import time
from datetime import timedelta

#An Object Oriented Approach to the NQueens Problem
#CISC 352, Queen's University Winter 2020

class nQueens:

    #Initialize the board

    def __init__(self, size):
        self.board=[None]*size
        self.rows=[i for i in range (size)]
        random.shuffle(self.rows)
        self.rowConf=[0]*size
        self.lDiagConf=[0]*(2*size-1)
        self.rDiagConf=[0]*(2*size-1)
        self.confRemain=0
        self.iterations=size*2
        self.resets=0
        self.start(size)
        self.solve(size)

    def start(self, size):
        for col in range(size):#i represents the ith column on the board
            if col==0:
                row=random.randint(0,size-1)#Generate a random int to place queen in rth row
                self.board[col]=row+1
                self.evalConf(row, col, size) #evaluate how many conflicts the queen has generated
            else:
                x=self.colConf(col,size)
                self.confRemain==x

    def evalConf(self, row, col, size):
        if (row-col)>=0:
            leftDiag=row-col
        else:
            leftDiag=(row-col)+(2*size-1)
        rightDiag=row+col
        numConf=self.rowConf[row]+self.lDiagConf[leftDiag]+self.rDiagConf[rightDiag]
        return numConf

    def solveConfUpdate(self, nRow, col, size):
        if (nRow-col)>=0:
            leftDiag=nRow-col
        else:
            leftDiag=(nRow-col)+(2*size-1)
        self.rowConf[nRow]+=1
        self.lDiagConf[leftDiag]+=1
        self.rDiagConf[nRow+col]+=1

    def conflictUpdate(self, row, col, size):
        if (row-col)>=0:
            leftDiag=row-col
        else:
            leftDiag=(row-col)+(2*size-1)
        self.rowConf[row]+=1
        self.lDiagConf[leftDiag]+=1
        self.rDiagConf[row+col]+=1
        self.rows.remove(row)
                    
    def colConf(self, col, size):
        confOne=[]
        confTwo=[]
        for row in self.rows:
            numConf=self.evalConf(row, col, size)
            if numConf==0:
                self.board[col]=row+1
                self.conflictUpdate(row,col,size)
                return 0
            if numConf==1:
                confOne.append(row)
            if numConf==2:
                confTwo.append(row)
        if len(confOne)==0:
            rVal=random.choice(confTwo)
            self.board[col]=rVal+1
            self.conflictUpdate(rVal, col, size)
            return 2
        rVal=random.choice(confOne)
        self.board[col]=rVal+1
        self.conflictUpdate(rVal, col, size)
        return 1

    def delQueen(self, oRow, col, size):
        if (oRow-col)>=0:
            lDiag=oRow-col
        else:
            lDiag=(oRow-col)+(2*size-1)
        self.lDiagConf[lDiag]-=1
        self.rDiagConf[rDiag]-=1
        self.rowConf[oRow]-=1
        if self.rowConf[oRow]==0:
            self.rows.append(oRow)

    def restart(self, size):
        self.board=[None]*size
        self.rows=[i for i in range (size)]
        random.shuffle(self.emptyRows)
        self.rowConf=[0]*size
        self.lDiagConf=[0]*(2*size-1)
        self.rDiagConf=[0]*(2*size-1)
        self.confRemain=0
        self.iterations=size*2
        self.start(size)
        self.solve(size)

    def solve (self, size):
        for i in range(self.iterations):
            
            if self.confRemain==0:
                return#Solution Found!
            else:
                randCol=random.randint(0,size-1) #look at a random col with 1 or more conflicts
                oRow=self.board(randCol)
                oRow-=1
                numConf= self.evalConf(oRow,randCol, size)-3
                while numConf <1:
                    randCol=random.randint(0,size-1)
                    oRow=self.board(randCol)
                    oRow-=1
                    numConf= self.evalConf(oRow,randCol, size)-3

                conflictsUpdated=False
                for newRow in self.rows:
                    numConf=self.calcConf(newRow, randCol, size)
                    if numConf==0:
                        self.board[randCol]=newRow+1
                        self.confRemain-=(self.evalConf(newRow, randCol, size)-3)
                        self.conflictUpdate(newRow, randCol, size)
                        self.delQueen(oRow, randCol, size)
                        conflictsUpdated=True
                        break

                if conflicsUpdated==False:
                    confTwo=[]
                    randRow=random.randint(0,size-1)
                    numConf=self.calcConf(randRow, randCol, size)
                    count=0
                    while numConf!=1:
                        randRow=random.randint(0,size-1)
                        numConf=self.calcConf(randRow, randCol, size)
                        if numConflicts==2:
                            confTwo.append(randRow)
                        Counter+=1
                        if counter == int(size/3):
                            break
                    if numConf==1:

                        self.board[randCol] = randRow + 1
                        self.confRemain -= ((self.calcConf(oRow, randCol, n) - 3) - numConf)
                        self.solveConfUpdate(randRow,randCol,size)
                        self.delQueen(oRow, randCol, size)
                    else:
                        if len(confTwo)>0:
                            randRow=random.choice(confTwo)
                            self.board[randCol] = randRow + 1
                            self.confRemain -= ((self.calcConf(oRow, randCol, size) - 3) - numConf)
                            self.solveConfUpdate(randRow,randCol,size)
                            self.delQueen(oRow, randCol, size)
                        else:
                            while numConf > (self.calcConf(oRow, randCol, n) - 3):
                                randRow=random.randint(0, n - 1)
                                numConf=calcConf(oRow, randCol, size)
                            self.board[randCol] = randRow + 1
                            self.confRemain -= ((self.calcConf(oRow, randCol, n) - 3) - numConf)
                            self.solveConfUpdate(randRow,randCol,size)
                            self.delQueen(oRow, randCol, size)
        self.resets+= 1
        print("restarting")
        self.restart(n)

def main():
    input = open("nqueens.txt")
    output = open("nqueens_out.txt", "w")
    lines = input.readlines()
    lines = [x.strip() for x in lines]
    lines = [int(i) for i in lines]
    for n in lines:
        print("Board size:\t\t"+str(n))
        start=time.time()
        board = nQueens(n)
        timeTaken=time.time()-start
        print("Solution Found in:\t\t"+str(timedelta(seconds=timeTaken)))
        #print("Remaining Conflicts: "+str(board.confRemain))
        print(board.board)
        print("Required # of Resets: "+str(board.resets))
        print("---")
                
        output.write(str(board.board) + "\n")
main()   
        
        
