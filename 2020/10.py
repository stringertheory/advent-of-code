import functools
import itertools
import math
import collections
import utils
    
def ok_seq(string):
    for i, group in itertools.groupby(string, key=lambda x: x=='0'):
        if len(list(group)) > 2:
            return False
    return True

def nc_slow(n_contig):
    if n_contig <= 2:
        return 1
    else:
        length = n_contig - 2
        result = 0
        for i in range(2**length):
            if ok_seq(format(i, 'b')):
                result += 1
        return result

@functools.lru_cache
def nc(n_contig):
    if n_contig <= 2:
        return 1
    elif n_contig == 3:
        return 2
    else:
        return 1 + nc(n_contig - 1) + nc(n_contig - 2)
    
    # return {
    #     1: 1,
    #     2: 1,
    #     3: 2,
    #     4: 4,
    #     5: 7,
    # }[n_contig]

for i in range(100):
    print(i, nc(i))
    
ints = []
for line in utils.iterstrip('input-10.txt'):
    ints.append(int(line))

builtin = max(ints) + 3
    
combos = 1
previous = 0
counter = collections.Counter()
ints.sort()
contig_groups = []
n_contig = 1
for j in list(sorted(ints)) + [builtin]:
    diff = j - previous
    counter[diff] += 1
    previous = j
    if diff == 1:
        n_contig += 1
    else:
        contig_groups.append(n_contig)
        n_contig = 1

res = [nc(i) for i in contig_groups]
print(res)
print(math.prod(res))
print([0] + list(sorted(ints)) + [builtin])
print(contig_groups)
print(math.prod(contig_groups))
print(counter)
print(counter[1] * counter[3])
print(combos)

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
    
