
"""wow, this was a hard one.

finished first in 20:57
second took a while, had to stop in between. finished after about an hour?

"""
import pprint
import itertools
import math
import collections
import datetime
import utils

from functools import reduce
# import networkx as nx
# from boltons import iterutils
# import traces
# from dateutil.parser import parse as date_parse

# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# itertools.combinations(abc, 2) -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4)) -> 4! possible orderings

class Moon:

    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = [x, y, z]
        self.v = [vx, vy, vz]

    def __repr__(self):
        return 'pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>'.format(
            *self.x, *self.v)

    def pe(self):
        return sum(abs(_) for _ in self.x)

    def ke(self):
        return sum(abs(_) for _ in self.v)

    def te(self):
        return self.pe() * self.ke()

moons = [
    Moon(14, 2, 8),
    Moon(7, 4, 10),
    Moon(1, 17, 16),
    Moon(-4, -1, 1),
]

# moons = [
#     Moon(-1, 0, 2),
#     Moon(2, -10, -7),
#     Moon(4, -8, 8),
#     Moon(3, 5, -1),
# ]

# moons = [
#     Moon(-8, -10, 0),
#     Moon(5, 5, 10),
#     Moon(2, -7, 3),
#     Moon(9, -8, -3),
# ]

def make_state(moons):
    state = []
    for a in moons:
        state.extend(a.x)
        state.extend(a.v)
    return state

def step(moons, n=None):

    states = [make_state(moons)]
    
    done = 0
    while True:
        for a, b in itertools.combinations(moons, 2):
            for i in [0, 1, 2]:
                if a.x[i] < b.x[i]:
                    a.v[i] += 1
                    b.v[i] -= 1
                elif a.x[i] > b.x[i]:
                    a.v[i] -= 1
                    b.v[i] += 1

        for a in moons:
            for i in [0, 1, 2]:
                a.x[i] += a.v[i]

        done += 1

        states.append(make_state(moons))
        print(done, moons[2].x[0])
        
        if not done % 100:
            print('nope', done, len(states))
            break
        
        state = tuple((tuple(a.x), tuple(a.v)) for a in moons)
        if state in states:
            # print(done)
            break
        else:
            states.add(state)

def find_periods(moons, n=1000000):

    states = [make_state(moons)]
    
    done = 0
    while done < n:
        for a, b in itertools.combinations(moons, 2):
            for i in [0, 1, 2]:
                if a.x[i] < b.x[i]:
                    a.v[i] += 1
                    b.v[i] -= 1
                elif a.x[i] > b.x[i]:
                    a.v[i] -= 1
                    b.v[i] += 1

        for a in moons:
            for i in [0, 1, 2]:
                a.x[i] += a.v[i]

        done += 1

        states.append(make_state(moons))

    return states

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

def find_period(values):
    for i in range(1, len(values)):
        if values[0:100] == values[i:(i+100)]:
            return len(values[0:i])
    return 0

periods = []
for index, tv in enumerate(zip(*find_periods(moons))):
    print('finding period', index)
    t = find_period(tv)
    print(t)
    periods.append(t)

periods = list(set(periods))
print(periods)
print(lcmm(*periods))

# step(moons, 1000)
# print()
# t = 0
# for i in moons:
#     print(i)
#     t += i.te()

# print(t)
