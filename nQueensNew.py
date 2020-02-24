#### Python 3
# -----------LIBRARY----------- #
import time
from datetime import timedelta
import random
# ----------------------------- #

def init(mainList, N):
    # mainList is the dictionary that contains
    # following information for a given index
    initMatrix = mainList[0]
    columnCounter = mainList[1]
    leftDiagonalCounter = mainList[2]
    rightDiagonalCounter = mainList[3]
    emptyColumns = mainList[4]
    
    # make a N sized list for each spot 
    for i in range(0,N): 
        initMatrix.append(0)
        columnCounter.append(0)
	
	# Except for the Diagonal Conflicts as explained latter in their function
        leftDiagonalCounter.append(0)
        leftDiagonalCounter.append(0)
        rightDiagonalCounter.append(0)
        rightDiagonalCounter.append(0)
	
	# This column will be used for creating a random board and hence needs to be started as [1,2,.....,N]
        emptyColumns.append(i+1)
     
    # Remove the extra zero as calculation only needs 2N - 1 size
    leftDiagonalCounter.remove(0) 
    rightDiagonalCounter.remove(0)

    # Creates a Random Board where Queens are not in the same column and row
    random.shuffle(emptyColumns)
	
    for row in range(0, N): 
        bestCol = getBestColumn(row, mainList, N)
        initMatrix[row] = bestCol
        if bestCol in emptyColumns:
            emptyColumns.remove(bestCol)

    return mainList
 
# -----------getBestColumn----------- #
# Returns: The best column position for the queen by:
# checkEmptyColumns if it finds zero conflict position
# randomColumnChecker: if it can find single conflict positiom
# ELSE returns the best position by getMatrix
# ----------------------------------- #
def getBestColumn(queen, mainList, N):
    originalColumn = int(mainList[0][queen])
    bestColumn = checkEmptyColumns(queen, mainList, N, originalColumn)


    if bestColumn == -1:
        bestColumn = randomColumnChecker(queen, mainList, N, originalColumn)
        if bestColumn == -1:
            bestColumn = getMatrix(queen, mainList, N, originalColumn)
            return bestColumn
        else:
            return bestColumn
    else:
        return bestColumn


# -----------updateConflicts----------- #
# Returns: mainList based on whether the New Column would be a better placement than the old column
# ------------------------------------- #

def updateConflicts(mainList, row, newColumn, oldColumn, N):
    columnCounter = mainList[1]
    leftDiagonalCounter = mainList[2]
    rightDiagonalCounter = mainList[3]

   #updating new getConflicts
    if newColumn != 0:
        columnCounter[newColumn-1] += 1
        leftDiagonalCounter[(N-1)-(row-(newColumn-1))] += 1
        rightDiagonalCounter[row + (newColumn - 1)] += 1

 
    if oldColumn != 0:
        columnCounter[oldColumn-1] -= 1
        leftDiagonalCounter[(N-1)-(row-(oldColumn-1))] -= 1
        rightDiagonalCounter[row + (oldColumn - 1)] -= 1

    return mainList
	

# -----------checkEmptyColumns----------- #
# Returns:
# --------------------------------------- #

def checkEmptyColumns(queen, mainList, N, originalColumn):
    initMatrix = mainList[0]
    emptyColumns = mainList[4]
    previousColumn = originalColumn
    for column in emptyColumns:
        initMatrix[queen] = column
        mainList = updateConflicts(mainList, queen, column, previousColumn, N)
        columnConflicts = getConflicts(queen, mainList, N)
        if columnConflicts == 0:
            return column
        previousColumn = column
        
    initMatrix[queen] = originalColumn
    
    mainList = updateConflicts(mainList, queen, originalColumn, previousColumn, N)
  

    return -1

# -----------randomColumnChecker----------- #
# Returns:
# ----------------------------------------- #
def randomColumnChecker(queen, mainList, N, originalColumn):
    initMatrix = mainList[0]
    k = 100
    previousColumn = originalColumn
    if N <= 100:
        k = int(N)
    randomColumnsList = random.sample(range(1, N+1), k)


    for column in randomColumnsList:
        initMatrix[queen] = column
        mainList = updateConflicts(mainList, queen, column, previousColumn, N)
        columnConflicts = getConflicts(queen, mainList, N)
        if columnConflicts == 1:
            return column
        previousColumn = column

    initMatrix[queen] = originalColumn

    mainList = updateConflicts(mainList, queen, originalColumn, column, N)
    
    return -1

# -----------getMatrix----------- #
# Returns:
# ------------------------------- #

def getMatrix(queen, mainList, N, originalColumn):
    initMatrix = mainList[0]
    previousColumn = originalColumn

    for column in range(1, N+1):
        initMatrix[queen] = column
        mainList = updateConflicts(mainList, queen, column, previousColumn, N)
        columnConflicts = getConflicts(queen, mainList, N)
        if columnConflicts == 1:
            return column
        previousColumn = column
        
    initMatrix[queen] = originalColumn
    mainList = updateConflicts(mainList, queen, originalColumn, previousColumn, N)

    return initMatrix[queen]


# -----------getConflicts----------- #
# Returns: Calculates all/total number of conflicts for a given Queen
# ---------------------------------- #

def getConflicts(queen, mainList, N):
    current = mainList[0]
    row = queen # for clarity
    column = current[row]
    totalConflicts = 0
    columnConflicts = mainList[1][column-1] 
    leftDiagConflicts = leftDiagonalConflicts(queen, mainList, N) 
    rightDiagConflicts = rightDiagonalConflicts(queen, mainList) 
    totalConflicts = (columnConflicts + leftDiagConflicts + rightDiagConflicts) - 3
    return totalConflicts 



# -----------constraints----------- #
# Returns: True/False based on whether the following 4 constraints have been voilated or not. 
# Only returns True if no two queens in the column, and only zero/one queen affect the left/right diagonal per index
# --------------------------------- #

def constraints(mainList):
    columnCounter = list(mainList[1])
    leftDiagonalCounter = list(mainList[2])
    rightDiagonalCounter = list(mainList[3])

    result = True
    columnCounter.sort()
    columnCounter.reverse()
    for c in columnCounter:
        if c > 1:
            return False
    leftDiagonalCounter.sort()
    leftDiagonalCounter.reverse()
    for ld in leftDiagonalCounter:
        if ld > 1:
            return False
    rightDiagonalCounter.sort()
    rightDiagonalCounter.reverse()
    for rd in rightDiagonalCounter:
        if rd > 1:
            return False
    return result


# -----------leftDiagonalConflicts----------- #
# Returns: For a given queen, calculates all its left Diagonal Conflicts. 1 for value means no conflict.
# Based on: https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645
# Left Diagonal for 'Q' Refers to:
# - - - -
# - Q - -
# - -  X -
# - - - -
# ------------------------------------------- #
def leftDiagonalConflicts(queen, mainList, N):
    current = mainList[0]
    row = queen 
    column = current[row]
    leftDiagonalCounter = mainList[2]
    leftDiagonalIndex = (N-1) - (row - (column-1) )
    leftDiagonalConflicts = leftDiagonalCounter[leftDiagonalIndex] # Do not count the current queen as a conflict
    return leftDiagonalConflicts 

# -----------rightDiagonalConflicts----------- #
# Returns: For a given queen, calculates all its right Diagonal Conflicts. 1 for value means no conflict.
# Based on: https://towardsdatascience.com/computing-number-of-conflicting-pairs-in-a-n-queen-board-in-linear-time-and-space-complexity-e9554c0e0645
# Right Diagonal for 'Q' Refers to (example for a 4 sized board) :
# - - - -
# - X - -
# - -  Q -
# - - - -
# -------------------------------------------- #
def rightDiagonalConflicts(queen, mainList):
    current = mainList[0]
    row = queen
    column = current[row]
    rightDiagonalCounter = mainList[3]
    rightDiagonalIndex = (row + (column - 1)) 
    rightDiagonalConflicts = rightDiagonalCounter[rightDiagonalIndex] # Do not count the current queen as a conflict
    return rightDiagonalConflicts 


# -----------legalMove----------- #
# Returns: Makes sure that after moving the queen, it does not get in conflict with the previous moved queens (True/False)
# ------------------------------- #
def legalMove(queenToRepair, queensMoved, potentialColumn, mainList, N):
    current = mainList[0]
    for movedQueen in queensMoved:
        movedQueenCol = current[movedQueen]
        if potentialColumn == movedQueenCol:
            return False
        else:
            leftDiagIndexMovedQueen = (N-1) - (movedQueen - (movedQueenCol-1) )
            leftDiagIndexQueenToRepair = (N-1) - (queenToRepair - (potentialColumn-1) )
            if leftDiagIndexMovedQueen == leftDiagIndexQueenToRepair:
                return False
            else:
                rightDiagIndexMovedQueen = (movedQueen + (movedQueenCol - 1))
                rightDiagIndexQueenToRepair = (queenToRepair + (potentialColumn - 1))
                if rightDiagIndexMovedQueen == rightDiagIndexQueenToRepair:
                    return False
    return True


# -----------minConflicts----------- #
# Returns:
# ---------------------------------- #

def minConflicts(N):
    mainList = [[],[],[],[],[]]
    mainList = init(mainList, N)
    current = mainList[0]
    columnCounter = mainList[1]
    emptyColumns = mainList[4]
    maxSteps = N

    if N < 1000:
        maxSteps = 1000
    
    currentStep = 0
    changed = True 
    queensUnmoved = random.sample(range(0, N), N)
    queensMoved = []
    queensLeft = N
    queenToRepair = 0
    noQueen = 0

    while currentStep <= maxSteps:
        if changed: # constrains below so that it's only called if necessary
            if constraints(mainList) == True:
                print("STEP: ", currentStep)
                
                return mainList

        if N > 500:
            queenToRepair = queensUnmoved[random.randint(0,queensLeft-1)]
        else:
            queenToRepair = random.randint(0,N-1)
            
        if getConflicts(queenToRepair, mainList, N) != 0:
            # repair Queen
            changed = True
            oldColumn = current[queenToRepair]
            bestCol = getBestColumn(queenToRepair, mainList, N)
            
            if N > 500:
                while legalMove(queenToRepair, queensMoved, bestCol, mainList, N) == False:
                    bestCol = getBestColumn(queenToRepair, mainList, N)

            current[queenToRepair] = bestCol
            if bestCol in emptyColumns:
                emptyColumns.remove(bestCol)
            if columnCounter[oldColumn-1] == 0:
                emptyColumns.append(oldColumn)
            
            currentStep += 1
            noQueen = 0

            if N > 500:
                queensLeft -= 1
                queensUnmoved.remove(queenToRepair)
                queensMoved.append(queenToRepair)
        else:
            noQueen += 1
            changed = False
                
    return mainList



# -----------solveNqueens----------- #
# Returns:
# ---------------------------------- #

def solveNqueens(N):
    max = 0

    # Different max steps, depends on size of N
    if N <= 1000:
        max = 10
    elif N > 1000 and N <= 100000: 
        max = 20
    elif N > 100000 and N <= 1000000: 
        max = 3
    else:
        print ("N is too large.")

    for i in range(0,max):
        currentAttempt = minConflicts(N)
        if constraints(currentAttempt) == True:
            break
        
    return currentAttempt[0]

def main():
    solutions = []
    with open("nqueens.txt", "r") as f:
        for line in f:
            N = int(line.rstrip())
            print("\n**********************************")
            print("Board-size: ", N)
            start=time.time()
            solutions.append(solveNqueens(N))
            timeTaken=time.time()-start
            print("Time Taken:\t"+str(timedelta(seconds=timeTaken)))
            print("**********************************")
    solutionsString = []
    
    for solution in solutions:
        solutionsString.append(str(solution))
        
    with open("nqueens_out.txt", "w") as f:
        f.write('\n'.join(solutionsString))

    print("\nPlease Find the solution in file: \"nqueens_out.txt\"")

main()
