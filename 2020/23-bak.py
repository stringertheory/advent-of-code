import sys
import copy
import pprint
import itertools
import math
import collections
import datetime
import utils

# import networkx as nx
# from boltons import iterutils
# import traces
# from dateutil.parser import parse as date_parse

# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# itertools.combinations(abc, 2) -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4)) -> 4! possible orderings

# 523764819

def rotate(array, value):
    n_rotate = array.index(value)
    for i in range(n_rotate):
        array.append(array.pop(0))
        
string = '389125467'
# string = '523764819'
cups = list(int(i) for i in string)
max_label = max(cups)
min_label = min(cups)

length = len(string)
n_moves = 10000000
cups.extend(list(range(max_label + 1, length + 1)))
max_label = max(cups)
min_label = min(cups)

neighbors = {}
for i, cup in enumerate(cups):
    neighbors[cup] = cups[(i + 1) % len(cups)]

current_value = cups[0]
for n_move in range(n_moves):
    # print('-- move {} --'.format(n_move + 1))
    # print('cups:', cups[:30])
    # print('cups   end:', cups[-30:])
    # print('current label', current_value)
    current_index = 0 #cups.index(current_value) # rotated!
    n = 3
    picked = []
    for i in range(n):
        picked.append(cups.pop((current_index + 1) % len(cups)))
    # print('pick up:', picked)
    found = False
    dest_label = current_value - 1
    while not found:
        try:
            dest_index = cups.index(dest_label)
        except:
            dest_label -= 1
            if dest_label < min_label:
                dest_label = max_label
        else:
            found = True
    # print('destination:', dest_label)
    for i in reversed(picked):
        cups.insert(dest_index + 1, i)

    current_value = cups[(cups.index(current_value) + 1) % len(cups)]
    rotate(cups, current_value)
    one_index = cups.index(1)

    rights = []
    for i in range(one_index, one_index + 3):
        rights.append(cups[i % len(cups)])
    # print('right', n_move, rights, math.prod(rights))
    # print(n_move, math.prod(rights), '"{}"'.format(rights))
    # print(n_move, rights[2], '"{}"'.format(rights))
    print(rights[1])#, rights[2], '"{}"'.format(n_move))
    # print()

order = []
one = cups.index(1)
for i in range(one + 1, one + len(cups)):
    order.append(cups[i % len(cups)])

print(''.join(str(i) for i in order[:80]), file=sys.stderr)
