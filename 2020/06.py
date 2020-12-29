
with open('input-06.txt') as infile:
    lines = infile.read().strip()
    
s = 0
t = 0
for group in lines.split('\n\n'):
    
    y = set()
    set_list = []
    for person in group.strip().split('\n'):
        pp = set(person)
        y.update(pp)
        set_list.append(pp)

    all_yes = set.intersection(*set_list)

    s += len(y)
    t += len(all_yes)
    
print(s)
print(t)

# ts = traces.TimeSeries()
    
# graph = nx.DiGraph()
# with open(filename) as infile:
#     for line in infile:
#         s, t = line.strip().split(')')
#         graph.add_edge(s, t)

# n = 0
# for node in graph.nodes:
#     n += len(list(nx.dfs_edges(graph, source=node)))
#     print(node, n)

# graph = nx.Graph()
# for line in iterstrip():
#     s, t = line.strip().split(')')
#     graph.add_edge(s, t)

# print(list(nx.shortest_path(graph, 'R85', 'YNY')))
# n = 0
# for node in graph.nodes:
#     n += len(list(nx.dfs_edges(graph, source=node)))
#     print(node, n)

