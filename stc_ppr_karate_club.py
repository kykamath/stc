import networkx as nx
import matplotlib.pyplot as plt
import math

def updateWeights(G):
  W = G.to_directed()
  outdegrees = W.out_degree()
  for (u,v, data) in W.edges(data=True): data['weight'] = 1/math.log(outdegrees[v]+2) 
  return W

def getAdamicAdar(graph, u):
  mf_neighbor_to_aa_score = {}
  neighbors = graph.neighbors(u)
  for n in neighbors:
    common_neighbors = set(graph.neighbors(n)).intersection(set(neighbors))
    mf_neighbor_to_aa_score[n] = sum(1/math.log(graph.degree(c)+2) for c in common_neighbors)
  for i in sorted(mf_neighbor_to_aa_score.items(), key=lambda t: -1*t[1]):
    print i

G=nx.karate_club_graph()

getAdamicAdar(G, 1)

# W = updateWeights(G)
# W_st = nx.stochastic_graph(W, weight="weight")
# for i in W_st.edges([1], data=True):
#   print i

# nx.draw_networkx(G, with_labels=True)
# plt.show()