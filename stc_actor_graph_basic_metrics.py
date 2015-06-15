import networkx as nx
import random

# cut -f1 actors_2500_0.65_6955_small | awk 'NR%2'| uniq

def load_graph(graph_file):
  graph = nx.Graph()
  for (u, v, w) in map(lambda l: map(int, l.strip().split()), open(graph_file)):
    graph.add_edge(u, v, {'orig_weight': w})
  return graph

def outputFormat(u, v, score): return "\t".join(map(str, [u, v, score])) + "\n"

def mutualFollow(graph, output_file_name):
  outputFile = open(output_file_name + "_mutualFollow", 'w')
  metric_name = "mutualFollow"
  for (u, v) in graph.edges():
    line = outputFormat(u, v, len(set(graph.neighbors(u)).intersection(graph.neighbors(v))))
    outputFile.write(line)
  outputFile.close()

def adamic_adar(graph, output_file_name): 
  outputFile = open(output_file_name + "_adamic_adar", 'w')
  for (u, v, score) in nx.adamic_adar_index(graph, graph.edges()): 
    line = outputFormat(u, v, score)
    outputFile.write(line)
  outputFile.close()

if __name__ == '__main__':
  graph_file = 'data/actors_2500.graph'
  num_edges = 700
  graph = load_graph(graph_file)
  
#   5619
#   67154
  
#   mutualFollow(graph, "data/actors_2500_%s"%num_edges)
  adamic_adar(graph, "data/actors_2500_%s"%num_edges)
  
#     print mutualFollow(u, v, graph)
