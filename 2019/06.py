import networkx as nx

import utils


for line in utils.iterstrip('input-06.txt'):
    line.split()
    
# graph = nx.DiGraph()
# with open(filename) as infile:
#     for line in infile:
#         s, t = line.strip().split(')')
#         graph.add_edge(s, t)

# n = 0
# for node in graph.nodes:
#     n += len(list(nx.dfs_edges(graph, source=node)))
#     print(node, n)

graph = nx.Graph()
for line in utils.iterstrip('input-06.txt'):
    s, t = line.strip().split(')')
    graph.add_edge(s, t)

print(list(nx.shortest_path(graph, 'R85', 'YNY')))
# n = 0
# for node in graph.nodes:
#     n += len(list(nx.dfs_edges(graph, source=node)))
#     print(node, n)
    
