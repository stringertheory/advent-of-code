import sys

def print_cups(neighbors, current_label):
    result = []
    neighbor = current_label
    while len(result) < len(neighbors):
        result.append(neighbor)
        neighbor = neighbors[neighbor]
    print('cups:', result)
        
# string = '389125467'
string = '523764819'
n_moves = 10000000

cups = list(int(i) for i in string)

length = 1000000
cups.extend(list(range(max(cups) + 1, length + 1)))

max_label = max(cups)
min_label = min(cups)

neighbors = {}
for i, cup in enumerate(cups):
    neighbors[cup] = cups[(i + 1) % len(cups)]

current_label = cups[0]
for n_move in range(n_moves):

    # print('-- move {} --'.format(n_move + 1))
    # print_cups(neighbors, current_label)
    # print('current label', current_label)

    picked = []
    neighbor = neighbors[current_label]
    while len(picked) < 3:
        picked.append(neighbor)
        neighbor = neighbors[neighbor]
    # print('pick up:', picked)
    
    dest_label = current_label - 1
    while True:
        if dest_label in picked:
            dest_label -= 1
        elif dest_label < min_label:
            dest_label = max_label
        else:
            break
    # print('destination:', dest_label)
    # print()

    neighbors[current_label] = neighbors[picked[2]]
    neighbors[picked[2]] = neighbors[dest_label]
    neighbors[dest_label] = picked[0]

    current_label = neighbors[current_label]
    
# print_cups(neighbors, current_label)

order = []
neighbor = neighbors[1]
for i in range(len(string) - 1):
    order.append(neighbor)
    neighbor = neighbors[neighbor]
print('part one:', ''.join(str(i) for i in order), file=sys.stderr)

r = neighbors[1]
rr = neighbors[r]
print('part two:', r, rr, r * rr)
