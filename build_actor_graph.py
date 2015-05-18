import itertools
from collections import defaultdict

raw_graph_file = "data/raw_actor_2500.graph"
output_graph_file = "data/actors_2500.graph"

edge_weight_map = defaultdict(int)
for line in open(raw_graph_file):
  for user_pair in itertools.combinations(line.strip().split(), 2):
    sorted_user_pair = sorted(user_pair)
    id = "%s_%s"%(sorted_user_pair[0],sorted_user_pair[1])
    edge_weight_map[id] = edge_weight_map.get(id, 0) + 1

output_graph = open(output_graph_file, "w")    
for (k,v) in edge_weight_map.iteritems():
  ids = k.split('_')
  output_graph.write("%s\t%s\t%s\n"%(ids[0], ids[1], v))
output_graph.close()
  