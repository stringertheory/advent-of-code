"""start one at: 10:50:30, end at 11:15:10
start two at 1:16, end at 2:15
"""
import utils

def print_state(area):
    total = 0
    depths = list(sorted(set(z for x, y, z in area)))
    for z in depths:
        print('depth', z)
        n = 0
        for y in range(5):
            for x in range(5):
                char = '.'
                if (x, y) == (2, 2):
                    char = '?'
                elif area[(x, y, z)]:
                    char = '#'
                    n += 1
                print(char, end='')
            print()
        print('n =', n)
        total += n
        print()
    print('total bugs', total)
        
def make_state(area):
    return tuple(v for k, v in sorted(area.items()))

def n_adjacent(area, x, y, z):
    result = 0
    for dx in [-1, 1]:
        result += int(area.get((x + dx, y, z), 0))
    for dy in [-1, 1]:
        result += int(area.get((x, y + dy, z), 0))
    return result

def n_adjacent_recursive(area, x, y, depth):
    neighbors = []
    for dx in [-1, 1]:
        nx, ny, nz = x + dx, y, depth
        if nx == -1:
            nx, ny, nz = 1, 2, depth - 1
            neighbors.append((nx, ny, nz))
        elif nx == 5:
            nx, ny, nz = 3, 2, depth - 1
            neighbors.append((nx, ny, nz))
        elif (nx, ny) == (2, 2):
            if dx == 1:
                nx = 0
            else:
                nx = 4
            for ny in range(5):
                neighbors.append((nx, ny, depth + 1))
        else:
            neighbors.append((nx, ny, nz))

    for dy in [-1, 1]:
        nx, ny, nz = x, y + dy, depth
        if ny == -1:
            nx, ny, nz = 2, 1, depth - 1
            neighbors.append((nx, ny, nz))
        elif ny == 5:
            nx, ny, nz = 2, 3, depth - 1
            neighbors.append((nx, ny, nz))
        elif (nx, ny) == (2, 2):
            if dy == 1:
                ny = 0
            else:
                ny = 4
            for nx in range(5):
                neighbors.append((nx, ny, depth + 1))
        else:
            neighbors.append((nx, ny, nz))
            
    result = 0
    for nx, ny, nz in neighbors:
        result += int(area.get((nx, ny, nz), False))
        # result += int(area[(nx, ny, nz)])
            
    # print('adj', (x, y, depth), neighbors, result)
    return result

def one_round(area, recursive=False):
    n_function = n_adjacent
    if recursive:
        n_function = n_adjacent_recursive
    new_area = {}
    for xy, value in sorted(area.items()):
        n = n_function(area, *xy)
        if value:
            new_area[xy] = False
            if n == 1:
                new_area[xy] = True
        else:
            new_area[xy] = False
            if n == 1 or n == 2:
                new_area[xy] = True
    return new_area

def biodiversity_rating(area):
    score = 0
    for i, (xy, value) in enumerate(sorted(area.items(), key=lambda i: (i[0][1], i[0][0]))):
        if value:
            score += (2 ** i)
    return score

input_filename = 'input-24.txt'

depth = 0
area = {}
for y, line in enumerate(utils.iterstrip(input_filename)):
    for x, char in enumerate(line):
        area[(x, y, depth)] = (char == '#')

states = set()
minute = 0
while True:
    area = one_round(area)
    minute += 1

    print('=== after {} ==='.format(minute))
    print_state(area)
    print()
    
    state = make_state(area)
    if state in states:
        break
    else:
        states.add(state)

print('part one:', biodiversity_rating(area))


n_minutes = 200
depth = 0
area = {}
for y, line in enumerate(utils.iterstrip(input_filename)):
    for x, char in enumerate(line):
        area[(x, y, depth)] = (char == '#')

for depth in range(1, n_minutes // 2 + 1):
    for y in range(5):
        for x in range(5):
            area[(x, y, depth)] = False
            area[(x, y, -depth)] = False
            
for minute in range(n_minutes):
    area = one_round(area, recursive=True)
    
print('=== after {} ==='.format(n_minutes))
print_state(area)
print()
