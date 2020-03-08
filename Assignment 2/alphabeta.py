#### Python 3
# -----------LIBRARY----------- #
import os
# ----------------------------- #


# ----------tree_generator----------- #
# Parameter: Tree information from the graph about children, root, leaves nodes
# Creates a general tree to run alpha-beta pruning on.
# ----------------------------------- #
def tree_generator(tree_info):
  print( tree_info )


def graph_solution(graph, graph_number):

  graph = graph.split()

  # Converts min-max info about each node into a dictionary
  # Works as nodes can only be letters - not characters
  node_info = dict(item.replace('(','').split(",") for item in graph[0][1:-2].split("),"))

  #Creating a general tree
  tree_generator(graph[1][1:-1])

  return "Graph "+ str(graph_number+ 1) + ": Score: 4; Leaf Nodes Examined: 6"

def main():

  #Reads the input file stores the data in variable named graphs
  input_file = open("alphabeta.txt", "r")

  #To ignore blank line
  graphs = (graph.rstrip() for graph in input_file)
  graphs = list(graph for graph in graphs if graph)

  input_file.close()

  # Removes any existing output file and creates a new one
  if os.path.exists("alphabeta_out.txt"):
    os.remove("alphabeta_out.txt")
  output_file= open("alphabeta_out.txt","a+")



  for graph in graphs:
    output_file.write(graph_solution(graph, graphs.index(graph)) + "\n")

  output_file.close()

main()
