import re
import collections
import utils

def innermost(ex):
    depth = collections.defaultdict(list)
    counter = 0
    for index, char in enumerate(ex):
        if char == '(':
            counter += 1
            depth[counter].append([index, None])
        elif char == ')':
            depth[counter][-1][1] = index + 1
            counter -= 1
    if depth:
        return depth[max(depth.keys())]
    else:
        return []

def domath(ex):

    clean = ex.replace('(', '')
    clean = clean.replace(')', '')
    
    numbers = [int(_) for _ in re.split('\+ | \*', clean)]
    operators = [_ for _ in clean if _ in {'+', '*'}]

    result = numbers.pop(0)
    for n, op in zip(numbers, operators):
        if op == '+':
            result += n
        elif op == '*':
            result *= n
        else:
            raise 'wut'

    return result

def domath2(ex):

    clean = ex.replace('(', '')
    clean = clean.replace(')', '')
    
    numbers = [int(_) for _ in re.split('\+ | \*', clean)]
    operators = [_ for _ in clean if _ in {'+', '*'}]

    if len(set(operators)) > 1:
        first_plus = operators.index('+')
        ns = [str(i) for i in numbers]
        ns[first_plus] = '(' + ns[first_plus]
        ns[first_plus + 1] = ns[first_plus + 1] + ')'
        chunks = [ns.pop(0)]
        for n, op in zip(ns, operators):
            chunks.append(op)
            chunks.append(n)
        return ev(' '.join(chunks), f=domath2)
    else:
    
        result = numbers.pop(0)
        for n, op in zip(numbers, operators):
            if op == '+':
                result += n
            elif op == '*':
                result *= n
            else:
                raise 'wut'

        return result

def ev(ex, maxd=10000, f=domath2):
    # print('raw', [ex])
    d = 0
    while innermost(ex):
        chunks = []
        pr = 0
        for l, r in innermost(ex):
            chunks.append(ex[pr:l])
            result = f(ex[l:r])
            # print([l, r, ex[pr:l], ex[l:r], result])
            chunks.append(str(result))
            pr = r

        # print('pr', pr, len(ex), ex[pr:])
        if pr < len(ex):
            # print(pr, ex[pr:])
            chunks.append(ex[pr:])

        # print('chunks', chunks)
        ex = ''.join(chunks)

        d += 1
        if d > maxd:
            raise 'shee'
    
    return f(ex)
                    
# a = ev('1 + 2 * 3 + 4 * 5 + 6')
# a = ev('1 + (2 * 3) + (4 * (5 + 6))')
# print(a)

a = ev('1 + 2')
a = ev('1 + 2 * 3 + 4 * 5 + 6')
# a = ev('5 * 6 + 1')
# print(a)
# raise 'STOP'

parsed = []
for line in utils.iterstrip('input-18.txt'):
    parsed.append(ev(line, f=domath))

print(sum(parsed))

parsed = []
for line in utils.iterstrip('input-18.txt'):
    parsed.append(ev(line, f=domath2))

print(sum(parsed))


