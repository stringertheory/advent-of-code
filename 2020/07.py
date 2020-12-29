import utils

import networkx as nx

n_unique = set()
graph = nx.DiGraph()
graph2 = nx.DiGraph()
for line in utils.iterstrip('input-07.txt'):
    sline = line.split('contain')
    outer = sline[0].rsplit(None, 1)[0].strip()
    inners = []
    if sline[1].strip() == 'no other bags.':
        inners = []
    else:
        for s in sline[1].split(','):
            first = s.rsplit(None, 1)[0].strip()
            n = int(first.split(None, 1)[0])
            inner = first.split(None, 1)[1].strip()
            inners.append((n, inner))

    n_unique.add(outer)
    for n, inner in inners:
        graph.add_edge(inner, outer)
        graph2.add_edge(outer, inner, weight=n)
        n_unique.add(inner)

print(len(nx.dfs_tree(graph, source='shiny gold').nodes) - 1)
        
def count_bags(g, source):
    n = 0
    for target in g[source]:
        weight = g.get_edge_data(source, target)['weight']
        n += weight
        n += weight * count_bags(g, target)
    return n

n = count_bags(graph2, 'shiny gold')
print(n)
