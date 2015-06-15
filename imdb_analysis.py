'''
Created on Jun 14, 2015

http://www.autonlab.org/autonweb/17433

@author: kkamath
'''
from _collections import defaultdict
import networkx as nx
import itertools

def buildGraph(mf_movie_to_actors_set, mf_actor_to_movies_set, min_movies):
  def valid_edge(u, v, mf_actor_to_movies_set):
    int = len(mf_actor_to_movies_set[u].intersection(mf_actor_to_movies_set[v]))
    return int > min_movies
    
  graph = nx.Graph()
  for movie, actors  in mf_movie_to_actors_set.iteritems():  
    for (u, v) in itertools.combinations(actors, 2): 
      if valid_edge(u, v, mf_actor_to_movies_set): graph.add_edge(u, v)
  print graph.number_of_edges(), graph.number_of_nodes()
  return graph  

def jakkard(u, v, mf_actor_to_movies_set):
  int = len(mf_actor_to_movies_set[u].intersection(mf_actor_to_movies_set[v]))+0.0
  uni = len(mf_actor_to_movies_set[u].union(mf_actor_to_movies_set[v]))+0.0
  return int/uni

# jakkard
def jakkard_analysis(graph):
  output_file = open("data/imdb_b__jakkard", "w")
  for (i, (u, v)) in enumerate(graph.edges_iter()): 
    print i
    output_file.write("\t".join(map(str, [u, v, jakkard(u, v, mf_actor_to_movies_set)])) + "\n") 
  output_file.close()

# mutual_follow
def mutual_follow(graph):  
  output_file = open("data/imdb_b__mutual_follow", "w")
  for (i, (u, v)) in enumerate(graph.edges_iter()): 
      print i
      output_file.write("\t".join(map(str, [u, v, len(list(nx.common_neighbors(graph, u, v)))])) + "\n") 
  output_file.close()

# adamin_adar
def adamic_adar(graph):
  output_file = open("data/imdb_b__adamic_adar", "w")
  for (i, (u, v, score)) in enumerate(nx.adamic_adar_index(graph, graph.edges_iter())): 
    print i
    output_file.write("\t".join(map(str, [u, v, score])) + "\n") 
  output_file.close()

def write_graph(graph, file_name):
  output_file = open(file_name, "w")
  for (u,v) in graph.edges_iter(): output_file.write("%s\t%s\n"%(u,v))
  output_file.close()

def load_graph(file_name):
  graph = nx.Graph()
  for (u,v) in map(lambda s: s.strip().split("\t"), open(file_name)): graph.add_edge(u,v)
  return graph

if __name__ == '__main__':
  
  graph_name = "imdb_b"
  min_movies = 5
  
#   raw_file = "data/imdb_s.csv" # edges: 4117535 nodes: 195865
  raw_file = "data/%s.csv"%graph_name
  mf_actor_to_movies_set = defaultdict(set)
  mf_movie_to_actors_set = defaultdict(set)
  for (movie, actor) in map(lambda l: l.strip().split(","), open(raw_file)): 
    mf_actor_to_movies_set[actor].add(movie)
    mf_movie_to_actors_set[movie].add(actor)
  graph = buildGraph(mf_movie_to_actors_set, mf_actor_to_movies_set, min_movies)
#   write_graph(graph, "data/%s_%s.graph"%(graph_name, min_movies))
  
  jakkard_analysis(graph)
  mutual_follow(graph)
  adamic_adar(graph)


