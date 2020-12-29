"""complete first in 16:21, second in 34:36

Would have placed! 58th for second star.

then refactored a bit.
"""
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


def read_input(filename):
    result = []
    for y, line in enumerate(utils.iterstrip(filename)):
        for x, char in enumerate(line):
            if char == '#':
                result.append((x, y))
    return result

asteroids = read_input('input-10.txt')

def calc_angle(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    angle = math.atan2(dy, dx)
    if angle < 0:
        angle = angle + 2 * math.pi
    return angle * 360 / (2 * math.pi)

def calc_distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx**2 + dy**2)

n_col = []
for a in asteroids:
    by_angle = collections.defaultdict(list)
    for b in asteroids:
        if b == a:
            continue
        angle = calc_angle(a, b)
        distance = calc_distance(a, b)
        by_angle[angle].append((distance, b))
    n_col.append((len(by_angle), a))

print(max(n_col))

monitor = max(n_col)[1]

by_angle = collections.defaultdict(list)
for b in asteroids:
    if b == monitor:
        continue
    angle = calc_angle(monitor, b)
    distance = calc_distance(monitor, b)
    by_angle[angle].append((distance, b))

sort = []
for angle, d in sorted(by_angle.items()):
    sort.append((angle, [_ for _ in sorted(d)]))
    
for index, (angle, d) in enumerate(sort):
    if angle >= 90:
        break

hit_no = 0
miss_no = 0
while miss_no <= len(sort):
    angle, ast_list = sort[index % len(sort)]
    if ast_list:
        hit_no += 1
        miss_no = 0
        print(hit_no, ast_list.pop(0))
    else:
        miss_no += 1
    index += 1

print(len(asteroids))
