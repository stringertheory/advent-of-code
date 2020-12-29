"""trying to find the alignment in the second part relied on seeing
that you could modify the step size of iteration when sub-parts of the
busses are aligned, and then get *much* more quickly to the answer.


"""
import math

from functools import reduce

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""   
    return reduce(lcm, args)

with open('input-13.txt') as infile:
    earliest = int(next(infile).strip())
    busses = dict((i, int(j)) for i, j in enumerate(next(infile).strip().split(',')) if j != 'x')

print(earliest)
print(busses)

next_time = {}
for bus_id in busses.values():
    t = 0
    while True:
        t += bus_id
        if t >= earliest:
            break
    next_time[bus_id] = t

n = min(next_time.values())
for bus_id, t in next_time.items():
    if t == n:
        dt = t - earliest
        print('part 1', dt * bus_id)


with open('input-13.txt') as infile:
    earliest = int(next(infile).strip())
    busses = dict((i, int(j)) for i, j in enumerate(next(infile).strip().split(',')) if j != 'x')
        
t = 0
dt = 1
while True:

    aligned = [bus for i, bus in busses.items() if (t + i) % bus == 0]
                        
    if len(aligned) == len(busses):
        print('part 2', t)
        break

    dt = math.prod(aligned)
    t += dt
