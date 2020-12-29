import utils

def decode(string):
    return int(string, 2)

# def decode(string, f, b):
#     number = 0
#     for index, char in enumerate(string):
#         p = len(string) - 1 - index
#         print(index, char, p, 2**p)
#         if char == f:
#             number += 0
#         elif char == b:
#             number += (2**p)
#         else:
#             raise 'Wut'
#     return number


def rc(line):
    row = decode(line[:7].translate(str.maketrans('FB', '01')))
    col = decode(line[7:].translate(str.maketrans('LR', '01')))
    return row, col

seat_ids = []
for index, line in enumerate(utils.iterstrip('input-05.txt')):
    row, col = rc(line)
    seat_id = row * 8 + col
    seat_ids.append((seat_id, line))

print(max(seat_ids))


previous = None
for seat_id, line in sorted(seat_ids):
    if previous is not None and abs(seat_id - previous) > 1:
        print(seat_id, line, seat_id - 1)
    previous = seat_id

r, c = rc('BFBFBFFLLL')
print(r * 8 + c)

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

