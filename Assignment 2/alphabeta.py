#### Python 3
# -----------LIBRARY----------- #
import os
from collections import defaultdict,deque
import sys
# ----------------------------- #


# ----------tree_generator----------- #
# Parameter: Tree information from the graph about children, root, leaves nodes
# Creates a general tree to run alpha-beta pruning on.
# Returns: General Tree
# ----------------------------------- #
def tree_generator(tree_info):
  tree_info= tree_info.replace('(','').replace('),','#').replace(',',':').replace('#',',').split(',')
  tree_info= list(item.split(":") for item in tree_info)

  # intilise
  d1 = defaultdict(list)

  for k, v in tree_info:
      d1[k].append(v)
  
  tree = dict((k, tuple(v)) for k, v in d1.items())
  return tree

# ----------children----------- #
# Parameter: 
# - tree: A multi-value dictionary containing info about each node's children
# - token: the node for which we want the children
# Creates a general tree to run alpha-beta pruning on.
# Returns: A list of all children with the token ordered by depth-right frst
# ----------------------------------- #
def children(token, tree):
    child_list = []
    to_crawl = deque([token])
    while to_crawl:
        current = to_crawl.popleft()
        child_list.append(current)
        try:
          node_children = tree[current]
        except KeyError:
          continue
        to_crawl.extend(node_children)
    return child_list


# ----------alpha_beta_pruning----------- #
# Parameter: 
# - tree: A multi-value dictionary containing info about's each node's children
# - node_info: Whether Each node is MIN or MAX
# Creates a general tree to run alpha-beta pruning on.
# Returns: Score and number of nodes visited
# ***Known issue***
# ALPHA_BETA_PRUNING NOT ITERATING TREE
# ----------------------------------- #
def alpha_beta_pruning(tree, node_info, alpha, beta,node,nodes_searched ):
  try:
    if (node_info[node] == "MAX"):
      tree_node_len = len(tree[node])
  except KeyError:
    if (node_info[node] == "MIN"):
      if (beta > int(tree[node][i])):
        beta = int(tree[node][i])
      return beta
    elif (node_info[node] == "MAX"):
      if (alpha < int(tree[node][i])):
        alpha = int(tree[node][i])
      return alpha

    for i in range(tree_node_len):
      print(tree[node][i])
      temp = alpha_beta_pruning(tree, node_info, alpha, beta,tree[node][i],nodes_searched )
      if (temp is None and alpha == -sys.maxsize - 1):
        return alpha
      else:
        alpha = max(alpha,temp )

          # Alpha Beta Pruning
      if (alpha <= beta ):
          return alpha
      else:
          i = tree_node_len
          break

  try:
    if (node_info[node] == "MIN"): #USELESS
      tree_node_len = len(tree[node])
  except KeyError:
    if (node_info[node] == "MIN"):
      if (beta > int(tree[node][i])):
        beta = int(tree[node][i])
      return beta
    elif (node_info[node] == "MAX"):
      if (alpha < int(tree[node][i])):
        alpha = int(tree[node][i])
      return alpha
    for i in range(tree_node_len):
      temp = alpha_beta_pruning(tree, node_info, alpha, beta,tree[node][i],nodes_searched )
      if (temp is None and beta == sys.maxsize):
        return beta
      else:
        beta = min(beta,temp)
        # Alpha Beta Pruning
        if (alpha <= beta ):
          return beta
        else:
          i = tree_node_len
          break



def graph_solution(graph, graph_number):

  graph = graph.split()

  # Converts min-max info about each node into a dictionary
  # Works as nodes can only be letters - not characters
  node_info = dict(item.replace('(','').split(",") for item in graph[0][1:-2].split("),"))

  #Creating a general tree
  tree = tree_generator(graph[1][1:-2])

  alpha = -sys.maxsize - 1
  beta = sys.maxsize
  node = list(tree.keys())[0]
  nodes_searched = 0
  temp = alpha_beta_pruning(tree, node_info,alpha,beta, node, nodes_searched)

  return "Graph "+ str(graph_number+ 1) + ": Score: " + str(temp) + "; Leaf Nodes Examined: " +  str(nodes_searched)

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
