import math

import utils

hill = []
for line in utils.iterstrip('input-03.txt'):
    hill.append(line)

def n_trees(hill, n_right, n_down):
    x = 0
    s = 0
    for y in range(0, len(hill), n_down):
        line = hill[y]
        if line[x % len(line)] == '#':
            s += 1
        x += n_right

    return s

print(n_trees(hill, 3, 1))

print(math.prod([
    n_trees(hill, 1, 1),
    n_trees(hill, 3, 1),
    n_trees(hill, 5, 1),
    n_trees(hill, 7, 1),
    n_trees(hill, 1, 2),
]))

    

