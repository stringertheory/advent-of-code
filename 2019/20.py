import copy
import pprint
import itertools
import math
import collections

import networkx as nx
from boltons import iterutils

def find_portals(full):

    inner_min = [0, 0]
    inner_max = [0, 0]
    for y, row in enumerate(full[2:-2]):
        if ' ' in row[2:-2]:
            inner_min[0] = row[2:-2].index(' ') + 2
            inner_max[0] = row[2:-2].rindex(' ') + 2
            inner_min[1] = y + 2
            break
    for y in range(len(full) - 3, 0, -1):
        if full[y][inner_min[0]] == ' ':
            inner_max[1] = y
            break

    # print(inner_min, inner_max)

    outer_portals = {}
    for x, aa in enumerate(zip(full[0], full[1]), -2):
        val = ''.join(aa).strip()
        if val:
            outer_portals[(x, 0)] = val
    for x, aa in enumerate(zip(full[-2], full[-1]), -2):
        val = ''.join(aa).strip()
        if val:
            outer_portals[(x, len(full) - 5)] = val
    for y in range(2, len(full) - 2 - 1):
        aa = full[y][:2]
        val = ''.join(aa).strip()
        if val:
            outer_portals[(0, y - 2)] = val
    for y in range(2, len(full) - 2 - 1):
        aa = full[y][-2:]
        val = ''.join(aa).strip()
        if val:
            outer_portals[(len(full[0]) - 5, y - 2)] = val

    inner_portals = {}
    for x, aa in enumerate(zip(full[inner_min[1]][inner_min[0]:inner_max[0]],
                               full[inner_min[1] + 1][inner_min[0]:inner_max[0]])):
        val = ''.join(aa).strip()
        if len(val) == 2:
            inner_portals[(x + inner_min[0] - 2, inner_min[1] - 2 - 1)] = val

    for x, aa in enumerate(zip(full[inner_max[1] - 1][inner_min[0]:inner_max[0]],
                               full[inner_max[1]][inner_min[0]:inner_max[0]])):
        val = ''.join(aa).strip()
        if len(val) == 2:
            inner_portals[(x + inner_min[0] - 2, inner_max[1] - 2 + 1)] = val
            
    for y in range(inner_min[1], inner_max[1] + 1):
        aa = full[y][inner_min[0]:(inner_min[0] + 2)]
        val = ''.join(aa).strip()
        if len(val) == 2:
            inner_portals[(inner_min[0] - 3, y - 2)] = val
        
    for y in range(inner_min[1], inner_max[1] + 1):
        aa = full[y][(inner_max[0] - 1):(inner_max[0] + 1)]
        val = ''.join(aa).strip()
        if len(val) == 2:
            inner_portals[(inner_max[0] - 1, y - 2)] = val
    
    return inner_portals, outer_portals
    

def read_maze(filename):

    full = []
    with open(filename) as infile:
        for line in infile:
            sline = line.strip('\n')
            if sline:
                full.append(sline)

    for y, row in enumerate(full):
        print('{:3d}'.format(y), row)
                
    maze = []
    for row in full[2:-2]:
        maze.append(row[2:-2])

    node_check1 = set()
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val == '.':
                node_check1.add((x, y))

    # print(len(node_check1), len(maze), len(maze[0]))
        
    # for y, row in enumerate(maze):
    #     print('{:3d}'.format(y), [row])
        
    graph = nx.Graph()
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val == '.':
                if (not y == 0) and maze[y - 1][x] == '.':
                    graph.add_edge((x, y), (x, y - 1))
                if (not y == (len(maze) - 1)) and maze[y + 1][x] == '.':
                    graph.add_edge((x, y), (x, y + 1))
                if (not x == 0) and maze[y][x - 1] == '.':
                    graph.add_edge((x, y), (x - 1, y))
                if (not x) == (len(row) - 1) and maze[y][x + 1] == '.':
                    graph.add_edge((x, y), (x + 1, y))
                    
    inner_portals, outer_portals = find_portals(full)
    links = collections.defaultdict(list)
    for xy, name in inner_portals.items():
        links[name].append(xy)
    for xy, name in outer_portals.items():
        links[name].append(xy)

    start = links.pop('AA')[0]
    end = links.pop('ZZ')[0]
    for name, xy_list in links.items():
        if len(xy_list) != 2:
            raise 'wut'

    return graph, inner_portals, outer_portals, links, start, end

def make_part_two_graph(graph, inner_portals, outer_portals, links, start, end):

    level0_outer_portals = [(start, outer_portals.pop(start)), (end, outer_portals.pop(end))]
    level0_all_portals = list(inner_portals.items()) + level0_outer_portals
    leveln_all_portals = list(inner_portals.items()) + list(outer_portals.items())

    portal_graph = nx.Graph()
    level = 0
    while True:

        print('level:', level)
        
        if level == 0:
            all_portals = level0_all_portals
        else:
            all_portals = leveln_all_portals
            
        for (xy1, name1), (xy2, name2) in itertools.combinations(all_portals, 2):
            try:
                path = nx.shortest_path(graph, xy1, xy2)
            except nx.exception.NetworkXNoPath:
                pass
            else:
                weight = len(path) - 1
                portal_graph.add_edge((name1, xy1, level), (name2, xy2, level), weight=weight)
        
        for name, xy_list in links.items():
            source, target = xy_list
            portal_graph.add_edge((name, source, level), (name, target, level + 1), weight=1)
            assert source in inner_portals
            assert target in outer_portals

        try:
            shorty = nx.shortest_path(portal_graph, ('AA', start, 0), ('ZZ', end, 0), weight='weight')
        except nx.exception.NetworkXNoPath:
            level += 1
        else:
            break

    # for e, edge in portal_graph.edges.items():
    #     print(e, edge)
        
    path_length = 0
    for a, b in iterutils.windowed(shorty, 2):
        edge = portal_graph.edges[(a, b)]
        path_length += edge['weight']
    print('part two:', path_length)

def main():
    graph, inner_portals, outer_portals, links, start, end = read_maze('input-20.txt')
    
    part_one_graph = copy.deepcopy(graph)
    for name, xy_list in links.items():
        part_one_graph.add_edge(*xy_list)

    print('part one:', len(list(nx.shortest_path(part_one_graph, start, end))) - 1)

    part_two_graph = make_part_two_graph(graph, inner_portals, outer_portals, links, start, end)


if __name__ == '__main__':
    main()
