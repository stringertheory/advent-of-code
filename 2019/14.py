"""start at 2:21
first star at 
second star at 3:49
"""
import pprint
import itertools
import math
import collections
import datetime
import utils

import networkx as nx

def balance(string):
    result = {}
    for part in string.split(','):
        count, mat = part.strip().split()
        count = int(count)
        result[mat.strip()] = count
    return result

unique = set()
reactions = []
for line in utils.iterstrip('input-14.txt'):
    left, right = line.split(' => ')
    l_balance = balance(left)
    r_mat, r_count = balance(right).popitem()
    reactions.append((l_balance, r_mat, r_count))
    if r_mat in unique:
        raise 'damn'
    elif r_mat == 'FUEL' and r_count != 1:
        raise 'shee'
    else:
        unique.add(r_mat)

def count_precursors(graph, node):
    if all([graph.edges[node, p]['visited'] for p in graph.successors(node)]):
        need = graph.nodes[node]['need']
        out = graph.nodes[node].get('weight', 0)
        for p in graph.predecessors(node):
            weight = graph.edges[p, node]['weight']
            graph.edges[p, node]['visited'] = True
            # print(node, need * weight, graph.nodes[node]['weight'])
            graph.nodes[p]['need'] += weight * math.ceil(need / out)
            count_precursors(graph, p)

start = int(1000000000000 / 485720)
fuel_need = start
while True:

    ore_need1 = None
    graph = nx.DiGraph()
    for l, r_mat, r_n in reactions:
        graph.add_node(r_mat, weight=r_n, need=0)
        for mat, n in l.items():
            graph.add_edge(mat, r_mat, weight=n, visited=None)

    graph.nodes['ORE']['need'] = 0
    graph.nodes['ORE']['weight'] = 1
    graph.nodes['FUEL']['need'] = fuel_need

    ordered = list(reversed(list(nx.topological_sort(graph))))
    fuel = ordered.pop(0)
    for node in ordered:
        need = 0
        for s in graph.successors(node):
            weight = graph.edges[node, s]['weight']
            need += weight * graph.nodes[s]['need']
        graph.nodes[node]['need'] = math.ceil(need / graph.nodes[node]['weight'])
    ore_need1 = graph.nodes['ORE']['need']
    
    graph = nx.DiGraph()
    for l, r_mat, r_n in reactions:
        graph.add_node(r_mat, weight=r_n, need=0)
        for mat, n in l.items():
            graph.add_edge(mat, r_mat, weight=n, visited=None)

    graph.nodes['ORE']['need'] = 0
    graph.nodes['ORE']['weight'] = 1
    graph.nodes['FUEL']['need'] = fuel_need

    count_precursors(graph, 'FUEL')
    ore_need2 = graph.nodes['ORE']['need']

    print(fuel_need, ore_need1, ore_need2)

    if ore_need2 >= 1000000000000:
        break
        
    fuel_need += 1
