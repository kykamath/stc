from collections import defaultdict

class EdgeInfo():
  def __init__(self, line):
    l = line.strip().split()
    self.source = int(l[0])
    self.numNeighbors = int(l[1])
    self.destination = int(l[2])
    self.ppr_weight = float(l[3])
    self.ppr_type = l[4]  
  def __str__(self):
    return "%s %s %s %s %s"%(self.source, self.destination, self.numNeighbors, self.ppr_weight, self.ppr_type)
  
# def convertLineToData(line):
#   l = line.strip().split()
#   return (l[0], int(l[1]), l[2], float(l[3]))

if __name__ == '__main__':
  alpha = 0.65
  
  graph = "edges_5867"
  valid_users = [18929196, 27731964, 1479414775]

#   graph = "kk"
#   valid_users = [1] 
    
#   input_file = open("data/%s_ppr_%s"%(graph, alpha))
  input_file = open("data/%s_ppr_with_and_without_edge_adamic_adar_%s"%(graph, alpha))
#   input_file = open("data/%s_%s"%(graph, alpha))
  mf_source_to_edge_info_with_edge = defaultdict(dict)
  mf_source_to_edge_info_without_edge = defaultdict(dict)
  for data in map(EdgeInfo, input_file.readlines()):
    if data.ppr_type=="with_edge": mf_source_to_edge_info_with_edge[data.source][data.destination] = data.ppr_weight
    else: mf_source_to_edge_info_without_edge[data.source][data.destination] = data.ppr_weight 
#       mf_source_to_edge_info[data.source][data.destination] = data.ppr_weight - 1.0/data.numNeighbors
    
  def scoreUserPair(src, dest):
    with_edge_ppr = mf_source_to_edge_info_with_edge[src][dest]
    without_edge_ppr = mf_source_to_edge_info_without_edge[src][dest]       
    #return (with_edge_ppr - without_edge_ppr) / (with_edge_ppr + without_edge_ppr)
    return without_edge_ppr
    
  for user in valid_users:
    output_file = open("data/%s_ppr_with_and_without_edge_adamic_adar_%s_%s_avg_new"%(graph, alpha, user), "w")
    dest_and_scores = [(dest, (scoreUserPair(user, dest) + scoreUserPair(dest, user))/2) 
                       for (dest, weight) in mf_source_to_edge_info_with_edge[user].items()]
    for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
  
    output_file = open("data/%s_ppr_with_and_without_edge_adamic_adar_%s_%s_max_new"%(graph, alpha, user), "w")
    dest_and_scores = [(dest, max(scoreUserPair(user, dest), scoreUserPair(dest, user)))  
                       for (dest, weight) in mf_source_to_edge_info_with_edge[user].items()]
    for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
     
    output_file = open("data/%s_ppr_with_and_without_edge_adamic_adar_%s_%s_min_new"%(graph, alpha, user), "w")
    dest_and_scores = [(dest, min(scoreUserPair(user, dest), scoreUserPair(dest, user)))  
                       for (dest, weight) in mf_source_to_edge_info_with_edge[user].items()]
    for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
    
    
#   valid_users = [1]
#     
#   for user in valid_users:
#     output_file = open("data/%s_%s_%s_avg_new"%(graph, alpha, user), "w")
#     dest_and_scores = [(dest, (scoreUserPair(user, dest) + scoreUserPair(dest, user))/2) 
#                        for (dest, weight) in mf_source_to_edge_info_with_edge[user].items()]
#     for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
#  
#     output_file = open("data/%s_%s_%s_max_new"%(graph, alpha, user), "w")
#     dest_and_scores = [(dest, max(scoreUserPair(user, dest), scoreUserPair(dest, user)))  
#                        for (dest, weight) in mf_source_to_edge_info_with_edge[user].items()]
#     for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
#     
#     output_file = open("data/%s_%s_%s_min_new"%(graph, alpha, user), "w")
#     dest_and_scores = [(dest, min(scoreUserPair(user, dest), scoreUserPair(dest, user)))  
#                        for (dest, weight) in mf_source_to_edge_info_with_edge[user].items()]
#     for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
    
    
    
    
#     output_file = open("data/%s_ppr_%s_%s_avg_new"%(graph, alpha, user), "w")
#     dest_and_scores = [(dest, (weight + mf_source_to_edge_info.get(dest, {}).get(user, 0.0))/2) 
#                        for (dest, weight) in mf_source_to_edge_info[user].items()]
#     for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
#       
#     output_file = open("data/%s_ppr_%s_%s_max_new"%(graph, alpha, user), "w")
#     dest_and_scores = [(dest, max(weight,  mf_source_to_edge_info.get(dest, {}).get(user, 0.0)))  
#                        for (dest, weight) in mf_source_to_edge_info[user].items()]
#     for (u, score) in sorted(dest_and_scores, key=lambda t: -t[1]): output_file.write("%s\t%s\n"%(u, score))
#   
  