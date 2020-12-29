import math
import utils

def parse_one(line):
    direction = line[0]
    count = int(line[1:])
    return direction, count

parsed = []
for chunk in utils.iterstrip('input-12.txt'):
    parsed.append(parse_one(chunk))

    
position = [0, 0]
direction = 0
for op, count in parsed:
    if op == 'N':
        position[1] += count
    elif op == 'S':
        position[1] -= count
    elif op == 'E':
        position[0] += count
    elif op == 'W':
        position[0] -= count
    elif op == 'L':
        direction += count
    elif op == 'R':
        direction -= count
    elif op == 'F':
        radian = direction * (math.pi / 180)
        x = int(round(count * math.cos(radian)))
        y = int(round(count * math.sin(radian)))
        position[0] += x
        position[1] += y
    else:
        raise 'WUT'
    
print(sum(abs(_) for _ in position))

position = [0, 0]
waypoint = [10, 1]
for op, count in parsed:
    if op == 'N':
        waypoint[1] += count
    elif op == 'S':
        waypoint[1] -= count
    elif op == 'E':
        waypoint[0] += count
    elif op == 'W':
        waypoint[0] -= count
    elif op == 'L':
        if count == 90:
            waypoint = [-waypoint[1], waypoint[0]]
        elif count == 180:
            waypoint = [-waypoint[0], -waypoint[1]]
        elif count == 270:
            waypoint = [waypoint[1], -waypoint[0]]
        else:
            raise
    elif op == 'R':
        if count == 90:
            waypoint = [waypoint[1], -waypoint[0]]
        elif count == 180:
            waypoint = [-waypoint[0], -waypoint[1]]
        elif count == 270:
            waypoint = [-waypoint[1], waypoint[0]]
        else:
            raise
    elif op == 'F':
        x = count * waypoint[0]
        y = count * waypoint[1]
        position[0] += x
        position[1] += y
    else:
        raise 'WUT'

print(sum(abs(_) for _ in position))
