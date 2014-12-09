from networkx.classes.function import common_neighbors
from collections import defaultdict
import math
import networkx as nx

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

def getSecondDegreeNodes(graph, u): 
  return (v2 
          for v1 in graph.neighbors(u) 
           for v2 in graph.neighbors(v1) if u != v2)

def fillAdamicScore(graph, node, mf_edge_to_score):
  for v in getSecondDegreeNodes(graph, node):
    edge_id = getEdgeId(node, v)
    if edge_id not in mf_edge_to_score: mf_edge_to_score[edge_id] = getAdamicScore(graph, node, v)    

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
    
def printStrongTies(graph, user_node, user_name, filter_follow = False):
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

#   printStrongTies(loadGraph('data/edges_5867'), '18929196', 'krishna_kamath', True) 
#   printStrongTies(loadGraph('data/edges_5867'), '1479414775', 'nayanakamath23', True) 
  printStrongTies(loadGraph('data/edges_5867'), '27731964', 'aneeshs', False)
  