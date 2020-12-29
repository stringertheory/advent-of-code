import collections
import utils

def n_occupied(layout, t='#'):
    counter = collections.Counter()
    for row in layout:
        for char in row:
            counter[char] += 1
    return counter
    
def n_occupied_adjacent(layout, x, y):
    n = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            else:
                i = x + dx
                j = y + dy
                if 0 <= i < len(layout) and 0 <= j < len(layout[0]):
                    v = layout[i][j]
                    if v == '#':
                        n +=1
    return n

def one_dir(layout, x, y, dx, dy):
    n = 0
    dxi = 0
    dyi = 0
    while True:
        dxi += dx
        dyi += dy
        i = x + dxi
        j = y + dyi
        # print(x, y, x + dxi, y + dyi, len(layout[x]), len(layout))
        if 0 <= i < len(layout) and 0 <= j < len(layout[0]):
            v = layout[x + dxi][y + dyi]
            if v == '#':
                n += 1
                break
            elif v == 'L':
                break
        else:
            break
                
    return n

def n_occupied_visible(layout, x, y):
    n = 0
    n += one_dir(layout, x, y, 1, 0)
    n += one_dir(layout, x, y, -1, 0)
    n += one_dir(layout, x, y, 0, 1)
    n += one_dir(layout, x, y, 0, -1)
    n += one_dir(layout, x, y, 1, 1)
    n += one_dir(layout, x, y, -1, -1)
    n += one_dir(layout, x, y, -1, 1)
    n += one_dir(layout, x, y, 1, -1)
        
    return n

    
def run(layout):
    shit = []
    new_layout = []
    for n_row, row in enumerate(layout):
        new_row = []
        shit_row = []
        for n_col, value in enumerate(row):
            shit_row.append(n_occupied_visible(layout, n_row, n_col))
            if value == 'L':
                if n_occupied_visible(layout, n_row, n_col) == 0:
                    new_row.append('#')
                else:
                    new_row.append(value)
            elif value == '#':
                if n_occupied_visible(layout, n_row, n_col) >= 5:
                    new_row.append('L')
                else:
                    new_row.append(value)
            else:
                new_row.append(value)
        new_layout.append(''.join(new_row))
        shit.append(shit_row)
    for row in shit:
        print(''.join(str(i) for i in row))
    return new_layout

def print_layout(layout):
    for row in layout:
        print(row)

parsed = []
for line in utils.iterstrip('input-11.txt'):
    parsed.append(line)

print(0, n_occupied(parsed))

i = 0
changed = True
while changed:
    i += 1
    before = tuple(parsed)
    print_layout(parsed)
    parsed = run(parsed)
    print(i, n_occupied(parsed))
    if before == tuple(parsed):
        changed = False

for row in parsed:
    print(row)

print()
print(n_occupied(parsed))
