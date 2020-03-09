# libraries
import math
import os

examined_count = 0
nodeList = []
connectionList = []
minNodes = []
maxNodes = []
def reset():
    global examined_count
    global nodeList
    global connectionList
    global minNodes
    global maxNodes
    examined_count = 0
    nodeList = []
    connectionList = []
    minNodes = []
    maxNodes = []

# transforms input file to tree
def buildTree(input):
    # reset variables
    reset()
    # save different parts of file in different variables
    inputSplit = input.split(" ")    # split input into MIN/MAX definitions and connection definitions
    nodes = inputSplit[0][2:-2].split("),(")    # node definition (name and min or max)
    connections = inputSplit[1][2:-2].split("),(")  # define connections

    # create list of nodes
    global nodeList

    for i in range(len(nodes)):
        nodeList.append(nodes[i].split(","))

    # create list of connections
    global connectionList
    for i in range(len(connections)):
        connectionList.append(connections[i].split(","))

    # create 2 lists,for MIN node elements and for MAX node elements
    global minNodes
    global maxNodes

    for minMax in nodeList:
        if minMax[1] == "MAX":
            maxNodes.append(minMax[0])
        else:
            minNodes.append(minMax[0])

def is_leaf(node):
    try:
        int(node)
        return True

    except ValueError:
        return False

def is_max_node(node):
    if node[0] in maxNodes:
        return True
    else:
        return False


def is_min_node(node):
    if node[0] in minNodes:
        return True
    else:
        return False

def is_root_node(node):
    if node[0] == nodeList[0]:
        return True
    else:
        return False


# implement given alpha_beta algorithm
def alpha_beta(current_node, alpha, beta):
    global examined_count

    if is_leaf(current_node):
        examined_count = examined_count+1
        return int(current_node)

    if is_max_node(current_node):
        for node in connectionList:
            if node[0] == current_node: # that means child node is node[1]
                alpha = max(alpha, alpha_beta(node[1], alpha, beta))
                if alpha >= beta:  # Cut off the rest of the child
                    return alpha
        return alpha


    if is_min_node(current_node):
        for node in connectionList:
            if node[0] == current_node:  # that means child node is node[1]
                beta = min(beta, alpha_beta(node[1], alpha, beta))
                if beta <= alpha:  # Cut off the rest of the child
                    return beta
        return beta

def main():

    # read input
    with open("alphabeta.txt","r") as f:
        inputs = f.readlines()

        # Removes any existing output file and creates a new one
    if os.path.exists("alphabeta_out.txt"):
        os.remove("alphabeta_out.txt")
    output_file = open("alphabeta_out.txt", "a+")

    for input in inputs:
        buildTree(input) # build the tree out of input file
        score = alpha_beta(connectionList[0][0], -math.inf, math.inf) # start algorithm with start configuration
        solution = "Graph: " + str(inputs.index(input)+1) + "; Score: " + str(score) + "; Leaf Nodes Examined: " + str(examined_count)
        print("##############################################")
        print(solution)
        print("##############################################\n")
        output_file.write(solution + "\n")
main()