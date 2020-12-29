"""did both stars in 18:10

then refactored some
"""

import pprint
import itertools
import math
import collections
import datetime
import utils

from termcolor import colored
# import networkx as nx
# from boltons import iterutils
# import traces
# from dateutil.parser import parse as date_parse

# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# itertools.combinations(abc, 2) -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4)) -> 4! possible orderings

def resolve(sequence, default):
    for i in sequence:
        if i != 2:
            return i
    return default

def read_elf_format(filename, width, height, default=2):

    with open(filename) as infile:
        s = infile.read().strip()
    
    layer_dict = collections.defaultdict(list)
    for index, char in enumerate(s):
        layer = index // (width * height)
        layer_dict[layer].append(int(char))

    histograms = []
    stacked = []
    for layer, data in sorted(layer_dict.items()):
        stacked.append(data)
        histograms.append(collections.Counter(data))

    # print(min((h[0], h[1] * h[2]) for h in histograms)) # part 1

    final = [[default for _ in range(width)] for _ in range(height)]
    for index, char_seq in enumerate(zip(*stacked)):
        x = index % width
        y = index // width
        value = resolve(char_seq, default)
        final[y][x] = value

    return final

def print_layer(layer):
    map = {
        0: 'blue',
        1: 'white',
        2: 'green',
    }
    for row in layer:
        for value in row:
            print(colored('█', map[value]), end='')
        print()

resolved = read_elf_format('input-08.txt', 25, 6)
print_layer(resolved)

    
