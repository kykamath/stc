from networkx.algorithms.approximation.vertex_cover import min_weighted_vertex_cover
import networkx as nx
import matplotlib.pyplot as plt

def loadGraph(fileName):
  
  def addLineToGraph(graph, line):
    data = line.strip().split()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    graph.add_edge(data[0], data[1])
  
  graph = nx.Graph()
  map(lambda l: addLineToGraph(graph, l), open(fileName)) 
  return graph


def getGraphDual(graph):
  
  def getEdgeId(edge):
    t = sorted(edge)
    return '%s_%s'%(t[0], t[1])
  
  def addEdgeToDual(graph, dualGraph, edge):
    u, v = edge
    uNeighbors = set(graph.neighbors(u)) - set([v])
    vNeighbors = set(graph.neighbors(v)) - set([u])
    uOpenTriangles = map(lambda n: ((u, v), (u, n)), (uNeighbors - vNeighbors))
    vOpenTriangles = map(lambda n: ((u, v), (v, n)), (vNeighbors - uNeighbors))
    openTriangles = uOpenTriangles + vOpenTriangles
    map(lambda t: dualGraph.add_edge(getEdgeId(t[0]), getEdgeId(t[1])), openTriangles)
  
  dualGraph = nx.Graph()
  map(lambda edge: addEdgeToDual(graph, dualGraph, edge), graph.edges_iter())
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


graph = loadGraph("demo_graph")
dualGraph = getGraphDual(graph)
print getVertexCoverGreedy(dualGraph)
print min_weighted_vertex_cover(getGraphDual(graph))


