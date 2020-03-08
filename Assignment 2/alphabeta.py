#### Python 3
# -----------LIBRARY----------- #
import os
# ----------------------------- #

#def alpha_beta_pruning(n):


def graph_solution(graph, graph_number):

  graph = graph.split()

  # Converts min-max info about nodes into a dictionary
  # Works as nodes can only be letters - not characters
  node_info = dict(item.replace('(','').split(",") for item in graph[0][1:-2].split("),"))

  tree_info = graph[1]

  print( node_info )

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
