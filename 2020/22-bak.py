import copy
import pprint
import itertools
import math
import collections
import datetime
import utils

# import networkx as nx
# from termcolor import colored
# from boltons import iterutils
# import traces
# from dateutil.parser import parse as date_parse

# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# itertools.combinations(abc, 2) -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4)) -> 4! possible orderings

with open('input.txt') as infile:
    s = infile.read().strip()

player1, player2 = s.split('\n\n')
p1 = []
for line in player1.splitlines()[1:]:
    sline = line.strip()
    if sline:
        p1.append(int(line))
p2 = []
for line in player2.splitlines()[1:]:
    sline = line.strip()
    if sline:
        p2.append(int(line))

print(p1, p2)
index = 0
while p1 and p2:
    card1 = p1.pop(0)
    card2 = p2.pop(0)
    if card1 > card2:
        p1.append(card1)
        p1.append(card2)
    elif card2 > card1:
        p2.append(card2)
        p2.append(card1)
        pass
    else:
        raise 'wut'
    index += 1

    
winner = p1 or p2

s = 0
for i, v in enumerate(reversed(winner), 1):
    print(i, v)
    s += i * v
print(p1, p2)
print(index)
print(s)


