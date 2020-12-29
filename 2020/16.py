import math
import collections
import utils

valid = collections.defaultdict(list)
for index, line in enumerate(utils.iterstrip('input-16.txt')):
    field, allowed = line.split(':')
    range1, range2 = allowed.split(' or ')
    low1, high1 = range1.split('-')
    low2, high2 = range2.split('-')
    for i in range(int(low1), int(high1) + 1):
        valid[i].append(field)
    for i in range(int(low2), int(high2) + 1):
        valid[i].append(field)
    if index > 18:
        break

my_ticket = [137,149,139,127,83,61,89,53,73,67,131,113,109,101,71,59,103,97,107,79]
    
all_invalid = []
valid_possibles = []
for index, line in enumerate(utils.iterstrip('input-16.txt')):
    if index < 25:
        continue
    numbers = [int(i) for i in line.split(',')]

    ticket_valid = True
    for n in numbers:
        if n not in valid:
            ticket_valid = False
            all_invalid.append(n)
            break

    if ticket_valid:
        possibles = [valid[i] for i in numbers]
        valid_possibles.append(possibles)

print(sum(all_invalid))
        
transpose = list(zip(*valid_possibles))
poss = []
for index, field in enumerate(transpose):
    narrowed = set.intersection(*tuple(set(i) for i in field))
    poss.append(narrowed)

def find_singles(p):
    result = {}
    for index, row in enumerate(p):
        if len(row) == 1:
            result[index] = row.pop()
    return result

answer = {}
while len(answer) < 20:
    singles = find_singles(poss)
    answer.update(singles)
    for key, val in singles.items():
        for row in poss:
            try:
                row.remove(val)
            except KeyError:
                pass

# print(answer)

vals = []
for i, n in enumerate(my_ticket):
    if answer[i].startswith('departure'):
        vals.append(n)

print(math.prod(vals))
