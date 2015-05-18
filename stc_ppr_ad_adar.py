import networkx as nx
import math

alpha = 0.65

def loadGraph(fileName):
  def addLineToGraph(graph, line):
    data = line.strip().split()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    graph.add_edge(int(data[0]), int(data[1]))
  graph = nx.Graph()
  map(lambda l: addLineToGraph(graph, l), open(fileName)) 
  return graph

def getPPRCandidates(graph, validUsers):
  candidates = []
  for u in validUsers: candidates+=(graph.neighbors(u) + [u])
  return list(set(candidates))

# def getPPR(candidate, graph, return_dict): 
#   print candidate
#   personalization = dict([(k, 0.0) for k in graph.nodes()])
#   personalization[candidate] = 1.0
#   mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
#   
#   neighbors = graph.neighbors(candidate)
#   num_neighbors = len(neighbors)
#   return_dict[candidate] = ["\t".join(map(str, [candidate, num_neighbors, k, mf_user_to_score[k]])) for k in neighbors]
  
def getPPRForUserPair(user1, user2, graph):
  print user1, user2
  personalization = dict([(k, 0.0) for k in graph.nodes()])
  personalization[user1] = 1.0
  graph.remove_edge(user1, user2)
  mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
  graph.add_edge(user1, user2)
  
  neighbors = graph.neighbors(user1)
  num_neighbors = len(neighbors)
  return ["\t".join(map(str, [user1, num_neighbors, user2, mf_user_to_score[user2], "without_edge"]))]

def getPPRForUserPairWithoutRemovingEdge(user1, user2, graph):
  print user1, user2
  personalization = dict([(k, 0.0) for k in graph.nodes()])
  personalization[user1] = 1.0
  mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
  
  neighbors = graph.neighbors(user1)
  num_neighbors = len(neighbors)
  return ["\t".join(map(str, [user1, num_neighbors, user2, mf_user_to_score[user2], "with_edge"]))]

def getPPR(candidate, valid_users, graph): 
    ppr = []
    for valid_user in valid_users:
      if (candidate in graph.neighbors(valid_user)): 
        ppr+=getPPRForUserPair(candidate, valid_user, graph) 
        ppr+=getPPRForUserPair(valid_user, candidate, graph)
        ppr+=getPPRForUserPairWithoutRemovingEdge(candidate, valid_user, graph) 
        ppr+=getPPRForUserPairWithoutRemovingEdge(valid_user, candidate, graph) 
    for p in ppr: print p
    return ppr
  
def updateWeights(G):
  W = G.to_directed()
  outdegrees = W.out_degree()
  for (u,v, data) in W.edges(data=True): data['weight'] = 1/math.log(outdegrees[v]+2) 
  return W

  
if __name__ == '__main__':
#   valid_users = [18929196, 27731964, 1479414775]
#   graph = "edges_5867"
#   graph_file = "data/%s"%(graph)
#   output_file = open("data/%s_ppr_with_and_without_edge_adamic_adar_%s"%(graph, alpha), "w")
#   graph = loadGraph(graph_file)

  valid_users = [1]
  output_file = open("data/%s_%s"%("kk", alpha), "w")
  graph=nx.karate_club_graph() 
  
  
  weighted_graph = updateWeights(graph)
   
  candidates = getPPRCandidates(weighted_graph, valid_users)
  for c in candidates:
    for s in getPPR(c, valid_users, weighted_graph): output_file.write(s + "\n")
