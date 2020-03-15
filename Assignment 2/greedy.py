import heapq
import copy

'''
Part#1.1: organize the given file into a grid from:
     1) pathA contains lines of the input of pathfinding_a.txt file.
        For example, [[x,x,x],[x,_,_],[x,s,g]] is the grid of the file with 3 lines and each line contains 3 elements
     2) pathSetA contains the start position of s and the end position of g.
        Like the example above, the list should be [(2, 1), (2,2)]
'''
def gridA():
    pathA = []
    pathSetA = [[None, None]]
    try:
        fileA = open("pathfinding_a.txt", 'r')
    except IOError:
        print("Error")
    else:
        for l in fileA:
            currentLine = l.strip('\n')
            #pathA is a list contians the sublist of lines of the file 
            if len(pathA) == 0: 
                pathA.append([])
            #aft reading the list element in the line
            if currentLine == "":
                pathA.append([])
                #read up all lines
                continue
            #provide the list which contains the position of the start and the end 
            pathA[-1].append([])
            
            for i in range(len(currentLine)):
                pathA[-1][-1].append(currentLine[i])
                #calculate the position of Start ("S")
                if currentLine[i] == "S":
                    if pathSetA[-1][0] == None:
                        pathSetA[-1][0] = (len(pathA[-1]) - 1, i)
                    elif pathSetA[-1][0] != None and pathSetA[-1][1] != None:
                        pathSetA.append([(len(pathA[-1]) - 1, i), None])
                #calculate the position of Start ("G")
                if currentLine[i] == "G":
                    if pathSetA[-1][1] == None:
                        pathSetA[-1][1] = (len(pathA[-1]) - 1, i)
                    elif pathSetA[-1][0] != None and pathSetA[-1][1] != None:
                        pathSetA.append([None, (len(pathA[-1]) - 1, i)])
        fileA.close()
    return pathA, pathSetA

'''
Part#1.2: organize the given file into a grid from:
     1) pathB contains lines of the input of pathfinding_b.txt file.
        For example, [[x,x,x],[x,_,_],[x,s,g]] is the grid of the file with 3 lines and each line contains 3 elements
     2) pathSetB contains the start position of s and the end position of g.
        Like the example above, the list should be [(2, 1), (2,2)] which means [(row),(column)]
'''
def gridB():
    pathB = []
    pathSetB = [[None, None]]
    try:
        fileB = open("pathfinding_b.txt", 'r')
    except IOError:
        print("Error")
    else:
        for l in fileB:
            currentLine = l.strip('\n')
            #pathA is a list contians the sublist of lines of the file 
            if len(pathB) == 0:
                pathB.append([])
            #aft reading the list element in the line
            if currentLine == "":
                pathB.append([])
                continue
            #provide the list which contains the position of the start and the end
            pathB[-1].append([])
            
            for i in range(len(currentLine)):
                pathB[-1][-1].append(currentLine[i])
                #calculate the position of Start ("S")
                if currentLine[i] == "S":
                    if pathSetB[-1][0] == None:
                        pathSetB[-1][0] = (len(pathB[-1]) - 1, i)
                    elif pathSetB[-1][0] != None and pathSetB[-1][1] != None:
                        pathSetB.append([(len(pathB[-1]) - 1, i), None])
                #calculate the position of Start ("G")
                if currentLine[i] == "G":
                    if pathSetB[-1][1] == None:
                        pathSetB[-1][1] = (len(pathB[-1]) - 1, i)
                    elif pathSetB[-1][0] != None and pathSetB[-1][1] != None:
                        pathSetB.append([None, (len(pathB[-1]) - 1, i)])
        fileB.close()
    return pathB, pathSetB


#consider mannHeuristic and chebHeuristic which will be used for pathfinding
def mannHeuristic(node, target):
    #the way to caluculate Mahattan distance 
    return abs(target[0] - node[0]) + abs(target[1] - node[1])

def chebHeuristic(node, target):
    #the way to caluculate Cheyshev distance 
    return max(abs(target[0] - node[0]), abs(target[1] - node[1]))

'''
Part#2: check neighbors of the element in the file：
        step1：put the availble neighbour into a list
        step2：use the ways above to find out the optimal neighbour to reach
'''
def checkNeighbors(element, grid, option):
    neighbors = []
    #the position of the element. e.g. (2, 1) -> (row = 2, column = 1)
    row = int(element[0]) 
    column = int(element[1])
    #option "A": up, down, left, and right.
    if option == "A":
        #up
        if row - 1 >= 0 and grid[row - 1][column] != "X":
            neighbors.append((row - 1, column))
        #down
        if row + 1 <= len(grid) - 1 and grid[row + 1][column] != "X":
            neighbors.append((row + 1, column))
        #left
        if column - 1 >= 0 and grid[row][column - 1] != "X":
            neighbors.append((row, column - 1))
        #right
        if column + 1 <= len(grid[row]) - 1 and grid[row][column + 1] != "X":
            neighbors.append((row, column + 1))

    #option "B": up, down, left, right, and diagonal.
    else:
        #up
        if row - 1 >= 0 and grid[row - 1][column] != "X":
            neighbors.append((row - 1, column))
        #down
        if row + 1 <= len(grid) - 1 and grid[row + 1][column] != "X":
            neighbors.append((row + 1, column))
        #left
        if column - 1 >= 0 and grid[row][column - 1] != "X":
            neighbors.append((row, column - 1))
        #right
        if column + 1 <= len(grid[row]) - 1 and grid[row][column + 1] != "X":
            neighbors.append((row, column + 1))
        #up-left
        if row - 1 >= 0 and column - 1 >= 0 and grid[row - 1][column - 1] != "X":
            neighbors.append((row - 1, column - 1))
        #up-right
        if row - 1 >= 0 and column + 1 <= len(grid[row]) - 1 and grid[row - 1][column + 1] != "X":
            neighbors.append((row - 1, column + 1))
        #down-left
        if row + 1 <= len(grid) - 1 and column - 1 >= 0 and grid[row + 1][column - 1] != "X":
            neighbors.append((row + 1, column - 1))
        #down-right
        if row + 1 <= len(grid) - 1 and column + 1 <= len(grid[row]) - 1 and grid[row + 1][column + 1] != "X":
            neighbors.append((row + 1, column + 1))
    return neighbors

'''
Part#3: Greedy algorithm
        use heap to search the target element and implement the algorithm
        use Mahattan distance and Cheyshev distance to find the optinal path 
'''

def greedy(grid, pathSet, option):
    start = pathSet[0]
    end = pathSet[1]
    queue = []
    #heapq.heappush(heap,item): push the item (0, (row,column)) into the heap
    heapq.heappush(queue, (0, start))
    #fromList is a dictionary to store the position of the node
    fromList = {}
    fromList[start] = None

    while len(queue) != 0:
        #heapq.heappop(heap,item): pop the item from the queue
        current = heapq.heappop(queue)
        #find the target
        if current[1] == end:
            break
        #check the neighbors around the start node
        neighbors = checkNeighbors(current[1], grid, option)

        #used the mannHeuristic and chebHeuristic to find the optimal path according to the neighbor list 
        while len(neighbors) != 0:
            if neighbors[-1] not in fromList:
                if option == "A":
                    priority = mannHeuristic(neighbors[-1], end)
                else:
                    priority = chebHeuristic(neighbors[-1], end)
                heapq.heappush(queue, (priority, neighbors[-1]))
                fromList[neighbors[-1]] = current
            del neighbors[-1]

    # walk through fromList dictionary to build the found path 
    pathSolution = []
    if fromList[current[1]] != None:
        nextNode = fromList[current[1]]
    else:
        return pathSolution
    while fromList[nextNode[1]] != None:
        pathSolution.append(nextNode[1])
        nextNode = fromList[nextNode[1]]
    return pathSolution



'''
Part#4: show the path in the pathfinding_out(a/b).txt file
'''

def findSolution(path, pathSet, option):
    solutionList = []
    currentList = []
    for i in range(len(path)):
        gPath = copy.deepcopy(path[i])
        currentSolution = greedy(gPath, pathSet[i], option)
        #mark the availble route in P's
        for item in currentSolution:
            gPath[item[0]][item[1]] = "P"
            
        result = gPath          
        currentList.append((result, "Greedy"))
        solutionList.append(currentList)
        #repeat to see the solution if there are more than one matrix in the file
        currentList = []
    return solutionList

def main():   
    pathA, pathSetA = gridA()
    pathB, pathSetB = gridB()
    solutionsA = findSolution(pathA, pathSetA, "A")
    solutionsB = findSolution(pathB, pathSetB, "B")
    fileList = ["pathfinding_a_out.txt", "pathfinding_b_out.txt"]
    for f in fileList:
        try:
            file = open(f, 'a')
        except IOError:
            print("Cannot open " + f)
        else:
            if f == "pathfinding_a_out.txt":
                for element in solutionsA:
                    for item in element:
                        file.write(str(item[1]) + '\n')
                        for i in range(len(item[0])):
                            row = ''.join(item[0][i])
                            file.write(row + '\n')
                    file.write('\n')
            else:
                 for element in solutionsB:
                    for item in element:
                        file.write(str(item[1]) + '\n')
                        for i in range(len(item[0])):
                            row = ''.join(item[0][i])
                            file.write(row + '\n')
                    file.write('\n')
    file.close()

main()



