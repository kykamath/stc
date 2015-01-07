from networkx.classes.function import common_neighbors
from collections import defaultdict
import math
import networkx as nx
import itertools

def loadGraph(fileName):
  def addLineToGraph(graph, line):
    data = line.strip().split()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
    graph.add_edge(data[0], data[1])
  graph = nx.Graph()
  map(lambda l: addLineToGraph(graph, l), open(fileName)) 
  return graph

def getEdgeId(u, v): 
  edge = sorted((u, v))
  return "%s\t%s"%(edge[0], edge[1])

def getEdge(edgeId): return map(lambda i: i, edgeId.split('\t'))

def getAdamicScore(graph, u, v):
  print u, v
  def getLog2(f):
    if f == 0 or f == 1: 
      print "getLog2 called with f=%s. This is not valid. Stopping the program."%f
      exit
    return math.log(f, 2)
  neighbors = list(common_neighbors(graph, u, v))
  if neighbors:
    total_score = sum(map(lambda n: 1/getLog2(len(graph.neighbors(n))), neighbors))
    return total_score/len(neighbors)
  else: 
    print "Number of common neighbors between u and v is 0. This is not valid. Stopping the program."
    exit
    
def getDispersionScore(graph, u, v):
  print u, v
  neighbors = list(common_neighbors(graph, u, v))
  neighbors_combinations = list(itertools.combinations(neighbors, 2))
  print neighbors_combinations
  if neighbors_combinations:
    total_edges = sum(graph.has_edge(u,v) for (u,v) in neighbors_combinations) + 0.0
    return total_edges/len(neighbors_combinations)
  else: return None
    
def getAdamicWithDispersionScore(graph, u, v, lmbda):
  if v in ['296462011', '18929196', '1290850711', '110426448', '2263652730', '1430955104']:
    print 'x'
  adamic_score = getAdamicScore(graph, u, v)
  dispersion_score = getDispersionScore(graph, u, v) 
  if dispersion_score: return (1-lmbda)*adamic_score + lmbda*(1-dispersion_score) 
  else: return (1-lmbda)*adamic_score
  
def getSecondDegreeNodes(graph, u): 
  return (v2 
          for v1 in graph.neighbors(u) 
           for v2 in graph.neighbors(v1) if u != v2)

def fillAdamicScore(graph, node, mf_edge_to_score):
  for v in getSecondDegreeNodes(graph, node):
    edge_id = getEdgeId(node, v)
    if edge_id not in mf_edge_to_score: mf_edge_to_score[edge_id] = getAdamicScore(graph, node, v)    

def fillAdamicWithDispersionScore(graph, node, mf_edge_to_score, lmdba):
  for v in getSecondDegreeNodes(graph, node):
    edge_id = getEdgeId(node, v)
    if edge_id not in mf_edge_to_score: mf_edge_to_score[edge_id] = getAdamicWithDispersionScore(graph, node, v, lmdba)

def printTopEdgesPerNode(mf_edge_to_score):
  mf_node_to_neighbor_w_score = defaultdict(dict)
  for (id, score) in mf_edge_to_score.iteritems():
    (u, v) = getEdge(id)
    mf_node_to_neighbor_w_score[u][v] = score
  for k, v in mf_node_to_neighbor_w_score.iteritems():
    print k, ','.join('%s:%s'%(t[0], t[1]) for t in sorted(v.items(), key=lambda t: t[1]))
    
def printTopFollowEdgesPerNode(graph, mf_edge_to_score):
  mf_node_to_neighbor_w_score = defaultdict(dict)
  for (id, score) in mf_edge_to_score.iteritems():
    (u, v) = getEdge(id)
    mf_node_to_neighbor_w_score[u][v] = score
  for k, v in mf_node_to_neighbor_w_score.iteritems():
    neighbors = graph.neighbors(k)
    sortedItems = sorted(v.items(), key=lambda t: t[1])
    sortedItems = filter(lambda t: t[0] in neighbors, sortedItems)
    print k, ','.join('%s:%s'%(t[0], t[1]) for t in sortedItems)
    
def printStrongTiesAdamicAdarDispersion(graph, user_node, user_name, filter_follow = False, lmbda = 0.5):
  mf_edge_to_score = {}
  mf_node_to_score = {}
  fillAdamicWithDispersionScore(graph, user_node, mf_edge_to_score, lmbda)
  for edge in mf_edge_to_score:
    (u, v) = getEdge(edge)
    node = None
    if u != user_node: node = u
    else: node = v
    mf_node_to_score[node] = mf_edge_to_score[edge]
  neighbors = graph.neighbors(user_node)
  sortedItems = sorted(mf_node_to_score.items(), key=lambda t: t[1])
  type = 'follow_not_filtered'
  if filter_follow: 
    type = 'follow_filtered'
    sortedItems = filter(lambda t: t[0] in neighbors, sortedItems)
  f = open('data/adamic_adar_dispersion_%s_%s_%s'%(user_name, type, lmbda), 'w')
  for i in ('%s:%s\n'%(t[0], t[1]) for t in sortedItems): f.write(i)
  f.close()

def printStrongTiesAdamicAdar(graph, user_node, user_name, filter_follow = False):
  mf_edge_to_score = {}
  mf_node_to_score = {}
  fillAdamicScore(graph, user_node, mf_edge_to_score)
  for edge in mf_edge_to_score:
    (u, v) = getEdge(edge)
    node = None
    if u != user_node: node = u
    else: node = v
    mf_node_to_score[node] = mf_edge_to_score[edge]
  neighbors = graph.neighbors(user_node)
  sortedItems = sorted(mf_node_to_score.items(), key=lambda t: t[1])
  type = 'follow_not_filtered'
  if filter_follow: 
    type = 'follow_filtered'
    sortedItems = filter(lambda t: t[0] in neighbors, sortedItems)
  f = open('data/adamic_adar_%s_%s'%(user_name, type), 'w')
  for i in ('%s:%s\n'%(t[0], t[1]) for t in sortedItems): f.write(i)
  f.close()

def printOptimizedStrongTies(graph, user_node, user_name, filter_follow = False):
#   def addNodeToCluster(node, graph, clustered_sub_graph, mf_node_to_cluster):
  def addNodeToCluster(node, graph, mf_node_to_cluster):
    # Get intersection of node's neighbors and current nodes in cluster
    # Get the number of clusters that the node belongs to.
    # If it is none then create a new cluster id for node
    # if it is one add the node to cluster
    # if it is more than one add merge cluster depending on how conductance
    nodes_neighbors = graph.neighbors(node)
    mf_cluster_distribution = defaultdict(int)
    for (n, cluster) in mf_node_to_cluster.iteritems(): 
      if n in nodes_neighbors: mf_cluster_distribution[cluster]+=1 
    selected_cluster = len(set(mf_node_to_cluster.values())) + 1
    if mf_cluster_distribution: selected_cluster = sorted(mf_cluster_distribution.items(), key=lambda t: t[1])[-1][0]
    mf_node_to_cluster[node] = selected_cluster
  def clusterNodes(node, graph, nodes, mf_node_to_cluster):
    sub_graph = graph.subgraph(nodes)
    graph.connectsub_graph.remove_node(node)
  type = 'follow_not_filtered'
  if filter_follow: type = 'follow_filtered'
  f = open('data/adamic_adar_%s_%s'%(user_name, type))
  mf_neighbor_to_stc_score = sorted(
                    ((t[0], float(t[1])) for t in (line.strip().split(':') for line in f)),
                    key=lambda t: t[1]
                  )
  mf_node_to_cluster = {}
  for (node, score) in mf_neighbor_to_stc_score:
    addNodeToCluster(node, graph, mf_node_to_cluster)
  mf_cluster_to_nodes = defaultdict(list)
  for (n, c) in mf_node_to_cluster.iteritems(): mf_cluster_to_nodes[c].append(n)
  for (c, nodes) in mf_cluster_to_nodes.items():
    print c, nodes

def getSTCProbabilities(graph):
  mf_edge_to_score = {}
  num_nodes = graph.number_of_nodes()
  for (i, v) in enumerate(graph.nodes()): 
#     print 'Processing %s of %s'%(i, num_nodes)
    fillAdamicScore(graph, v, mf_edge_to_score)
#   printTopEdgesPerNode(mf_edge_to_score)
  printTopFollowEdgesPerNode(graph, mf_edge_to_score)
 
if __name__ == '__main__':
#   getSTCProbabilities(loadGraph('data/demo_graph'))  
#   getSTCProbabilities(loadGraph('data/edges_5867')) 

#   printStrongTiesAdamicAdar(loadGraph('data/edges_5867'), '1479414775', 'nayanakamath23', True) 
  printStrongTiesAdamicAdarDispersion(loadGraph('data/edges_5867'), '1479414775', 'nayanakamath23', True, 0.0) 
  
#   printStrongTiesAdamicAdar(loadGraph('data/edges_5867'), '18929196', 'krishna_kamath', True) 
  printStrongTiesAdamicAdarDispersion(loadGraph('data/edges_5867'), '18929196', 'krishna_kamath', True, 0.0) 

#   printStrongTiesAdamicAdar(loadGraph('data/edges_5867'), '27731964', 'aneeshs', True) 
  printStrongTiesAdamicAdarDispersion(loadGraph('data/edges_5867'), '27731964', 'aneeshs', True, 0.0) 


  