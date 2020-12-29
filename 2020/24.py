import math
import collections
import utils

#   nw  ne
   
# w        e

#   sw  se
R3 = math.sqrt(3)
hexes = {
    'w': (-2, 0),
    'e': (2, 0),
    'nw': (-1, 1),
    'ne': (1, 1),
    'sw': (-1, -1),
    'se': (1, -1),
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

def adjacent_colors(tiles, key):
    counter = collections.Counter()
    x, y = key
    for d, (dx, dy) in hexes.items():
        new_key = x + dx, y + dy
        counter[tiles.get(new_key, 'white')] += 1
    return counter

def one_round(tiles):
    tile_keys = set()
    for key, color in tiles.items():
        if color == 'black':
            tile_keys.add(key)
            for d, (dx, dy) in hexes.items():
                x, y = key
                new_key = x + dx, y + dy
                tile_keys.add(new_key)

    # print('lens', len(tiles), len(tile_keys))

    new_colors = {}
    n_black = 0
    for key in tile_keys:
        color = tiles.get(key, 'white')
        if color == 'black':
            n_black += 1
        nabe_count = adjacent_colors(tiles, key)
        # print(key, color, nabe_count)
        new_colors[key] = color
        if color == 'black' and (nabe_count['black'] == 0 or nabe_count['black'] > 2):
            # print('BLACK -> WHITE', key, color, nabe_count)
            new_colors[key] = "white"
        if color == 'white' and nabe_count['black'] == 2:
            # print('WHITE -> BLACK', key, color, nabe_count)
            new_colors[key] = 'black'

    # print('n_black', n_black)
    # print(list(new_colors.values()).count('black'))
    return new_colors

PRECISE = 10
ROUND = 5


parsed = []
for line in utils.iterstrip('input-24.txt'):
    item = parse_line(line)
    parsed.append(item)


tiles = {}
n_flips = collections.Counter()
for flips in parsed:
    x, y = 0, 0
    for flip in flips:
        d = hexes[flip]
        x += d[0]
        y += d[1]

    r_key = x, y
    n_flips[r_key] += 1
    
    color = tiles.get(r_key, "white")
    if color == "black":
        color = "white"
    elif color == "white":
        color = "black"
    else:
        raise 'wut'
    
    tiles[r_key] = color

# for i, n in n_flips.most_common():
#     print(i, n)
    
print(0, list(tiles.values()).count('black'))
for r in range(100):
    day = r + 1
    tiles = one_round(tiles)
    print(day, list(tiles.values()).count('black'))

