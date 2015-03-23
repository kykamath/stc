import networkx as nx
from multiprocessing import Process, Manager

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
  return candidates

def getPPR(candidate, graph, return_dict): 
  personalization = dict([(k, 0.0) for k in graph.nodes()])
  personalization[candidate] = 1.0
  mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
  
  neighbors = graph.neighbors(candidate)
  num_neighbors = len(neighbors)
  return_dict[candidate] = ["\t".join(map(str, [candidate, num_neighbors, k, mf_user_to_score[k]])) for k in neighbors]

# def getPPR(candidate, graph): 
#   personalization = dict([(k, 0.0) for k in graph.nodes()])
#   personalization[candidate] = 1.0
#   mf_user_to_score = nx.pagerank(graph, alpha=alpha, personalization = personalization)
#   
#   neighbors = graph.neighbors(candidate)
#   num_neighbors = len(neighbors)
#   return ["\t".join(map(str, [candidate, num_neighbors, k, mf_user_to_score[k]])) for k in neighbors]

# if __name__ == '__main__':
#   valid_users = [18929196, 27731964]
#   graph = "edges_5867"
#   graph_file = "data/%s"%(graph)
#   graph = loadGraph(graph_file)
#   candidates = getPPRCandidates(graph, valid_users)
#   for v in getPPR(18929196, graph):
#     print v

if __name__ == '__main__':
  valid_users = [18929196, 27731964]
  graph = "edges_5867"
  graph_file = "data/%s"%(graph)
  output_file = open("data/%s_ppr_%s"%(graph, alpha), "w")
  
  graph = loadGraph(graph_file)
  
  manager = Manager()
  return_dict = manager.dict()
  jobs = []
  for candidate in getPPRCandidates(graph, valid_users):
    p = Process(target=getPPR, args=(candidate, graph, return_dict))
    jobs.append(p)
    p.start()

  for proc in jobs: proc.join()
  
  for scores in return_dict.values():
    for s in scores: output_file.write(s + "\n")
  output_file.close()

