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

#   nw  ne
   
# w        e

#   sw  se
R3 = math.sqrt(3)
hexes = {
    'w': (-1, 0),
    'e': (1, 0),
    'nw': (-1/2, R3),
    'ne': (1/2, R3),
    'sw': (-1/2, -R3),
    'se': (1/2, -R3),
}


def parse_line(line):
    allowed = {'w', 'e', 'nw', 'ne', 'sw', 'se'}
    previous = None
    index = 0
    directions = []
    while index < len(line):
        chunk = line[index]
        if chunk in allowed:
            directions.append(chunk)
            index += 1
        else:
            chunk = line[index:(index + 2)]
            assert chunk in allowed
            directions.append(chunk)
            index += 2
    return directions

def adjacent_colors(tiles, p_key):
    counter = collections.Counter()
    px, py = p_key
    for d, (dx, dy) in hexes.items():
        nx, ny = px + dx, py + dy
        r_key = round(nx, ROUND), round(ny, ROUND)
        counter[tiles.get(r_key, 'white')] += 1
    return counter

def one_round(tiles, tiles_f):
    tile_keys = set()
    for (rx, ry), color in tiles.items():
        fx, fy = tiles_f[(rx, ry)]
        l_key = round(fx, PRECISE), round(fy, PRECISE)
        tile_keys.add(l_key)
        for d, (dx, dy) in hexes.items():
            nx, ny = fx + dx, fy + dy
            l_key = round(nx, PRECISE), round(ny, PRECISE)
            tile_keys.add(l_key)

    # print('lens', len(tiles), len(tile_keys))

    new_colors = {}
    new_f = {}
    n_black = 0
    for px, py in tile_keys:
        r_key = round(px, ROUND), round(py, ROUND)
        color = tiles.get(r_key, 'white')
        if color == 'black':
            n_black += 1
        nabe_count = adjacent_colors(tiles, (px, py))
        new_colors[r_key] = color
        new_f[r_key] = (px, py)
        if color == 'black' and (nabe_count['black'] == 0 or nabe_count['black'] > 2):
            # print('BLACK -> WHITE', r_key, color, nabe_count)
            new_colors[r_key] = "white"
        elif color == 'white' and nabe_count['black'] == 2:
            # print('WHITE -> BLACK', r_key, color, nabe_count)
            new_colors[r_key] = 'black'

    # print('n_black', n_black)
    # print(list(new_colors.values()).count('black'))
    return new_colors, new_f

PRECISE = 10
ROUND = 5


parsed = []
for line in utils.iterstrip('input.txt'):
    item = parse_line(line)
    parsed.append(item)



tiles_f = {}
tiles = {}
n_flips = collections.Counter()
for flips in parsed:
    x, y = 0, 0
    for flip in flips:
        d = hexes[flip]
        x += d[0]
        y += d[1]

        
    rx = round(x, ROUND)
    ry = round(y, ROUND)
    r_key = rx, ry
    n_flips[r_key] += 1
    
    color = tiles.get(r_key, "white")
    if color == "black":
        color = "white"
    elif color == "white":
        color = "black"
    else:
        raise 'wut'
    
    tiles[r_key] = color
    tiles_f[r_key] = (x, y)
    
print(0, list(tiles.values()).count('black'))
for r in range(100):
    day = r + 1
    tiles, tiles_f = one_round(tiles, tiles_f)
    print(day, list(tiles.values()).count('black'))

