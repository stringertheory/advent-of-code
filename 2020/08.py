import utils
import copy

def run(ops):
    run = set()
    index = 0
    acc = 0
    while index < len(ops):
        op, count = ops[index]
        if index in run:
            return False, acc
            break
        else:
            run.add(index)
        if op == 'acc':
            acc += count
            index += 1
        elif op == 'jmp':
            index += count
        elif op == 'nop':
            index += 1
        else:
            raise 'wut'

    return True, acc
    
def one_run(all_ops, switch_index=0):
    ops = copy.deepcopy(all_ops)
    if ops[switch_index][0] == 'nop':
        ops[switch_index][0] = 'jmp'
    elif ops[switch_index][0] == 'jmp':
        ops[switch_index][0] = 'nop'
    return run(ops)


all_ops = []
for line in utils.iterstrip('input-08.txt'):
    op, count = line.split()
    count = int(count)
    all_ops.append([op, count])

    
for i in range(len(all_ops)):
    s, acc = one_run(all_ops, i)
    if s:
        print(i, s, acc)

        
# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# -> [(False, ['a', ])]
# itertools.combinations(abc, 2)
# -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4))
# -> 4! possible orderings

