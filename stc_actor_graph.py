import networkx as nx
import random

def load_graph(graph_file):
  graph = nx.Graph()
  for (u, v, w) in map(lambda l: map(int, l.strip().split()), open(graph_file)):
    graph.add_edge(u, v, {'orig_weight': w})
  return graph

def get_edges(graph, num_edges): return random.sample(graph.edges(), num_edges)

def getPPRForUserPairWithRemovingEdge(user1, user2, graph, alpha):
  print user1, user2
  personalization = dict([(k, 0.0) for k in graph.nodes()])
  personalization[user1] = 1.0
  graph.remove_edge(user1, user2)
  mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
  graph.add_edge(user1, user2)
  
  neighbors = graph.neighbors(user1)
  num_neighbors = len(neighbors)
  return ["\t".join(map(str, [user1, num_neighbors, user2, mf_user_to_score[user2], "without_edge"]))]

def getPPRForUserPairWithoutRemovingEdge(user1, user2, graph, alpha):
  print user1, user2
  personalization = dict([(k, 0.0) for k in graph.nodes()])
  personalization[user1] = 1.0
  mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
  
  neighbors = graph.neighbors(user1)
  num_neighbors = len(neighbors)
  return ["\t".join(map(str, [user1, num_neighbors, user2, mf_user_to_score[user2], "with_edge"]))]

def getPPR(graph, edge, alpha): 
  (user1, user2) = edge
  ppr = []
  ppr+=getPPRForUserPairWithRemovingEdge(user1, user2, graph, alpha) 
  ppr+=getPPRForUserPairWithRemovingEdge(user2, user1, graph, alpha)
  ppr+=getPPRForUserPairWithoutRemovingEdge(user1, user2, graph, alpha) 
  ppr+=getPPRForUserPairWithoutRemovingEdge(user2, user1, graph, alpha) 
  for p in ppr: print p
  return ppr


if __name__ == '__main__':
  graph_file = 'data/actors_2500.graph'
  alpha = 0.65
  num_edges = 1
  
  graph = load_graph(graph_file)
  candidate_edges = get_edges(graph, num_edges)
  output_file = open("data/%s_%s_%s"%("actors_2500", alpha, len(candidate_edges)), "w")
  
  for edge in candidate_edges:
    for s in getPPR(graph, edge, alpha): output_file.write(s + "\n")
  
#   print graph.number_of_nodes()
#   print graph.number_of_edges()
 