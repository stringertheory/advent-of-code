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
play1 = []
for line in player1.splitlines()[1:]:
    sline = line.strip()
    if sline:
        play1.append(int(line))
play2 = []
for line in player2.splitlines()[1:]:
    sline = line.strip()
    if sline:
        play2.append(int(line))

        
def one_round(p1, p2, recursive=True):

    print('game')

    index = 1
    previous_rounds = set()
    while p1 and p2:

        print('round', index)
        print('p1', p1)
        print('p2', p2)
        
        round_key = tuple(p1 + ['butt'] + p2)
        if round_key in previous_rounds:
            return [True], []
        
        previous_rounds.add(round_key)

        card1 = p1.pop(0)
        card2 = p2.pop(0)

        print('p1 plays', card1)
        print('p2 plays', card2)
        
        subgame_winner = None
        if recursive:
            if len(p1) >= card1 and len(p2) >= card2:
                print('recurse')
                # print(card1, len(p1[:card1]))
                # raise 'STOP'
                s1, s2 = one_round(p1[:card1], p2[:card2], recursive=recursive)
                subgame_winner = s1 or s2

        if subgame_winner is not None:
            if s1:
                print('p1 wins round', index)
                p1.append(card1)
                p1.append(card2)
            elif s2:
                print('p2 wins round', index)
                p2.append(card2)
                p2.append(card1)
            else:
                raise 'wut'
        else:
            if card1 > card2:
                print('p1 wins round', index)
                p1.append(card1)
                p1.append(card2)
            elif card2 > card1:
                print('p2 wins round', index)
                p2.append(card2)
                p2.append(card1)
            else:
                raise 'wut'
            
        index += 1
        print()

    if p1:
        print('p1 wins game')
    else:
        print('p2 wins game')
        
    return p1, p2

p1, p2 = one_round(play1, play2, recursive=True)
    
winner = p1 or p2

s = 0
for i, v in enumerate(reversed(winner), 1):
    s += i * v
    print(i, v, s)
    
print(p1, p2)
print('result', s)
