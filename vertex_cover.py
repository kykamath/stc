from itertools import groupby
from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover
import networkx as nx
import matplotlib.pyplot as plt
import sys
import random
from scipy.stats.stats import pearsonr
import numpy as np
from collections import defaultdict

def loadGraph(fileName):
  
  def addLineToGraph(graph, line):
    data = line.strip().split()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    graph.add_edge(data[0], data[1])
  
  graph = nx.Graph()
  map(lambda l: addLineToGraph(graph, l), open(fileName)) 
  return graph

def loadGraphWithWeight(fileName):
  
  def addLineToGraph(graph, line):
    data = line.strip().split()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    graph.add_edge(data[0], data[1], {'w': float(data[2])})
  
  graph = nx.Graph()
  map(lambda l: addLineToGraph(graph, l), open(fileName)) 
  return graph

def writeDualGraph(graph, fileName):
  f = open(fileName+'_dual', 'w')
  for e in graph.edges_iter():
    f.write('%s\t%s\n'%(e[0], e[1]))
  f.close()
  
def writeVertexCover(vertexCover, fileName):
  f = open(fileName+'_vertex_cover', 'w')
  for v in vertexCover: f.write('%s\n'%v)
  f.close()

def getEdgeId(edge):
  t = sorted(edge)
  return '%s_%s'%(t[0], t[1])  

def getGraphDual(graph):
  
  def addEdgeToDual(graph, dualGraph, edgeIt):
    it, edge = edgeIt
    print 'Adding edge to dual graph: ', it+1, edge
    u, v = edge
    uNeighbors = set(graph.neighbors(u)) - set([v])
    vNeighbors = set(graph.neighbors(v)) - set([u])
    uOpenTriangles = map(lambda n: ((u, v), (u, n)), (uNeighbors - vNeighbors))
    vOpenTriangles = map(lambda n: ((u, v), (v, n)), (vNeighbors - uNeighbors))
    openTriangles = uOpenTriangles + vOpenTriangles
    map(lambda t: dualGraph.add_edge(getEdgeId(t[0]), getEdgeId(t[1])), openTriangles)
  
  dualGraph = nx.Graph()
  map(lambda edgeIt: addEdgeToDual(graph, dualGraph, edgeIt), enumerate(graph.edges_iter()))
  return dualGraph

# This method modifies input graph.
def getVertexCoverGreedy(graph):

  def maxDegreeNode(g): 
    items = sorted(g.degree().items(), key=lambda t: t[1])
    if len(items) > 0 and items[-1][1] != 0: return items[-1][0]
    else: return None

  vertexCoverSet = set()
  nextVertexToRemove = maxDegreeNode(graph)
  iteration = 1
  while nextVertexToRemove != None:
    print 'Generating vertex cover. Iteration: ', iteration
    iteration = iteration + 1
    vertexCoverSet.add(nextVertexToRemove)
    graph.remove_node(nextVertexToRemove)
    nextVertexToRemove = maxDegreeNode(graph)
  return vertexCoverSet

#
# python vertex_cover.py data/edges_5867_2
#
# 1.3319152651
# 1.3501473505
# (0.018432481710418454, 0.57022048147957038)

def calculateDifferenceInRealGraphWeights(fileName):
  graph = loadGraphWithWeight(fileName)
  
  dualGraph = getGraphDual(graph)
  writeDualGraph(dualGraph, inputGraphFile)
  
  loadGraph()
  
  vertexCover = min_weighted_vertex_cover(dualGraph)
  writeVertexCover(vertexCover, inputGraphFile)
  
  edgeIdToWeightMap = map(lambda e: (getEdgeId(e[:2]), e[2]['w']), graph.edges_iter(data=True))
  
  weakEdges = []
  strongEdges = []
  for e in graph.edges_iter(data=True):
    edgeId = getEdgeId(e[:2])
    weight = e[2]['w']
    if edgeId in vertexCover: weakEdges.append(weight)
    else: strongEdges.append(weight)
 
  numElements = -1
  if len(weakEdges) > len(strongEdges): numElements = len(strongEdges)
  else: numElements = len(weakEdges)
 
  print np.mean(weakEdges)
  print np.mean(strongEdges)
  print pearsonr(random.sample(weakEdges, numElements), random.sample(strongEdges, numElements))
  
  

def printLabeledEdges(fileName):
  graph = loadGraphWithWeight(fileName)
  
  dualGraph = loadGraph(fileName+'_dual')
#   writeDualGraph(dualGraph, inputGraphFile)
  
  vertexCover = min_weighted_vertex_cover(dualGraph)
  writeVertexCover(vertexCover, inputGraphFile)
  
  edgeIdToWeightMap = map(lambda e: (getEdgeId(e[:2]), e[2]['w']), graph.edges_iter(data=True))
  
  weakEdges = []
  strongEdges = []
  for e in graph.edges_iter(data=True):
    edgeId = getEdgeId(e[:2])
    weight = e[2]['w']
    if edgeId in vertexCover: print edgeId.replace('_', ' '), '0' 
    else: print edgeId.replace('_', ' '), '1'
 
def printDegreeWithStrongTies(fileName):
  graph = loadGraphWithWeight(fileName)
  labeledGraph = loadGraphWithWeight(fileName+'_labeled')
  degreeWithStrongTiesCount = defaultdict(int)
  for e in labeledGraph.edges(data=True):
    degreeWithStrongTiesCount[e[0]]+=e[2]['w']
    degreeWithStrongTiesCount[e[1]]+=e[2]['w']
  
  for k,v in graph.degree().iteritems():
    print k, v, degreeWithStrongTiesCount.get(k, 0.0)
 
def degreeDistribution(fileName):
  graph = loadGraphWithWeight(fileName)
  
#   graph = nx.Graph()
  degrees = sorted(graph.degree().values())
  degreeDist = map(lambda (k, v): (k, len(list(v))), groupby(degrees, lambda k: k))
  x, y = zip(*sorted(degreeDist, key = lambda t: t[0]))
  
  plt.loglog(x, y, 'o', c = 'k')
  plt.xlabel('Num. of neighbors')
  plt.ylabel('Num. of nodes')
  plt.show()


if __name__ == '__main__':
  inputGraphFile = sys.argv[1]
#   graph = loadGraph(inputGraphFile)
#   dualGraph = getGraphDual(graph)
#   writeDualGraph(dualGraph, inputGraphFile)
#   writeVertexCover(getVertexCoverGreedy(dualGraph), inputGraphFile)

#   writeVertexCover(getVertexCoverGreedy1(loadGraph(inputGraphFile)), inputGraphFile)

#   writeVertexCover(min_weighted_vertex_cover(loadGraph(inputGraphFile)), inputGraphFile)

#   calculateDifferenceInRealGraphWeights(inputGraphFile)
#   printLabeledEdges(inputGraphFile)
#   degreeDistribution(inputGraphFile)
  printDegreeWithStrongTies(inputGraphFile)
  


