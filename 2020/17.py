import utils

def n_neighbors(board, x, y, z, w, value):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dw in [-1, 0, 1]:
                    if not (dx, dy, dz, dw) == (0, 0, 0, 0):
                        if board.get((x + dx, y + dy, z + dz, w + dw), '.') == value:
                            count += 1
    return count

parsed = []
for line in utils.iterstrip('input-17.txt'):
    item = line
    parsed.append(item)

board = {}
for y, row in enumerate(parsed):
    for x, char in enumerate(row):
        z = 0
        w = 0
        board[(x, y, z, w)] = char
        
def run(board):
    # new = copy.deepcopy(board)
    new = {}
    x_max = max(x for (x, y, z, w) in board)
    y_max = max(y for (x, y, z, w) in board)
    z_max = max(z for (x, y, z, w) in board)
    w_max = max(w for (x, y, z, w) in board)
    x_min = min(x for (x, y, z, w) in board)
    y_min = min(y for (x, y, z, w) in board)
    z_min = min(z for (x, y, z, w) in board)
    w_min = min(w for (x, y, z, w) in board)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                for w in range(w_min - 1, w_max + 2):
                    char = board.get((x, y, z, w), '.')
                    if char == '#':
                        if n_neighbors(board, x, y, z, w, '#') in [2, 3]:
                            new[(x, y, z, w)] = '#'
                        else:
                            new[(x, y, z, w)] = '.'
                    else:
                        if n_neighbors(board, x, y, z, w, '#') == 3:
                            new[(x, y, z, w)] = '#'
                        else:
                            new[(x, y, z, w)] = '.'
    return new

print(board)
print(list(board.values()).count('#'))

for i in range(6):
    board = run(board)
    print(board)
    print(list(board.values()).count('#'))

