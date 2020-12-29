import utils

path = [[0, 0]]

def path(inst):
    x_pos = 0
    y_pos = 0
    result = [(x_pos, y_pos)]
    for i in inst:
        d = i[0]
        n = int(i[1:])
        for j in range(n):
            if d == 'R':
                x_pos += 1
            elif d == 'L':
                x_pos -= 1
            elif d == 'D':
                y_pos -= 1
            elif d == 'U':
                y_pos += 1
            result.append((x_pos, y_pos))
    return result

paths = []
for line in utils.iterstrip('input-03.txt'):
    paths.append(path(line.split(',')))

path1 = paths[0]
path2 = paths[1]

for x, y in set(path1).intersection(set(path2)):
    print(x, y, path1.index((x, y)) + path2.index((x, y)))
