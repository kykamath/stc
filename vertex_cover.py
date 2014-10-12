from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover
import networkx as nx
import matplotlib.pyplot as plt
import sys

def loadGraph(fileName):
  
  def addLineToGraph(graph, line):
    data = line.strip().split()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    graph.add_edge(data[0], data[1])
  
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
  

def getGraphDual(graph):
  
  def getEdgeId(edge):
    t = sorted(edge)
    return '%s_%s'%(t[0], t[1])
  
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
  while nextVertexToRemove != None:
    vertexCoverSet.add(nextVertexToRemove)
    graph.remove_node(nextVertexToRemove)
    nextVertexToRemove = maxDegreeNode(graph)
  return vertexCoverSet


if __name__ == '__main__':
  inputGraphFile = sys.argv[1]
  graph = loadGraph(inputGraphFile)
  dualGraph = getGraphDual(graph)
  writeDualGraph(dualGraph, inputGraphFile)
  writeVertexCover(getVertexCoverGreedy(dualGraph), inputGraphFile)
  
# print min_weighted_vertex_cover(getGraphDual(graph))


