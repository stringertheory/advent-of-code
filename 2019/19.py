import functools
import time
import random
import pprint
import itertools
import math
import collections
import datetime
import utils
from termcolor import colored

import networkx as nx

from boltons import iterutils

    
class Intcode:

    params = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3,
    }
    
    def __init__(self, filename):
        for line in utils.iterstrip(filename):
            self.code = [int(_) for _ in line.split(',')]
        self.code += [0] * (100 * len(self.code))
        self.orig_code = list(self.code)
        
        self.index = 0
        self.relative_base = 0

    def reset(self):
        self.code = list(self.orig_code)
        self.index = 0
        self.relative_base = 0
        
    def get(self, parameter, mode):
        if mode == 0:
            return self.code[parameter]
        elif mode == 1:
            return parameter
        elif mode == 2:
            return self.code[self.relative_base + parameter]
        else:
            raise 'wut get mode'

    def set(self, parameter, value, mode):
        if mode == 0:
            self.code[parameter] = value
        elif mode == 2:
            self.code[self.relative_base + parameter] = value
        else:
            raise 'wut set mode'
        
    def run(self, inputs):
        outputs = []
        while True:
            instruction = '{:05d}'.format(self.code[self.index])
            opcode = int(instruction[-2:])
            m1 = int(instruction[-3])
            m2 = int(instruction[-4])
            m3 = int(instruction[-5])
            if opcode == 1:
                p1, p2, p3 = self.code[(self.index + 1):(self.index + 4)]
                v1 = self.get(p1, m1)
                v2 = self.get(p2, m2)
                self.set(p3, v1 + v2, m3)
                self.index += 4
            elif opcode == 2:
                p1, p2, p3 = self.code[(self.index + 1):(self.index + 4)]
                v1 = self.get(p1, m1)
                v2 = self.get(p2, m2)
                self.set(p3, v1 * v2, m3)
                self.index += 4
            elif opcode == 3:
                p1 = self.code[self.index + 1]
                # val = input('which way? ').strip()
                # if val == 'a':
                #     val = -1
                # elif val == 'p':
                #     val = 1
                # else:
                #     val = 0
                # self.set(p1, val, m1)
                self.set(p1, inputs.pop(0), m1)
                self.index += 2
            elif opcode == 4:
                p1 = self.code[self.index + 1]
                v1 = self.get(p1, m1)
                self.index += 2
                # print('output: ', v1)
                return v1
            elif opcode == 5:
                p1 = self.code[self.index + 1]
                p2 = self.code[self.index + 2]
                if self.get(p1, m1):
                    self.index = self.get(p2, m2)
                else:
                    self.index += 3
            elif opcode == 6:
                p1 = self.code[self.index + 1]
                p2 = self.code[self.index + 2]
                if not self.get(p1, m1):
                    self.index = self.get(p2, m2)
                else:
                    self.index += 3
            elif opcode == 7:
                p1, p2, p3 = self.code[(self.index + 1):(self.index + 4)]
                self.set(p3, int(self.get(p1, m1) < self.get(p2, m2)), m3)
                self.index += 4
            elif opcode == 8:
                p1, p2, p3 = self.code[(self.index + 1):(self.index + 4)]
                self.set(p3, int(self.get(p1, m1) == self.get(p2, m2)), m3)
                self.index += 4
            elif opcode == 9:
                p1 = self.code[self.index + 1]
                self.relative_base += self.get(p1, m1)
                self.index += 2
            elif opcode == 99:
                raise StopIteration
            else:
                msg = 'wut opcode `{}`'.format(opcode)
                raise Exception(msg)
        return outputs
    

I = Intcode('input-19.txt')

@functools.lru_cache(maxsize=None)
def get(x, y):
    result = I.run([x, y])
    I.reset()
    return result

def find_approximate_slopes(y):
    """take a slice at specific y value to find two slopes."""
    prev = 0
    n_switches = 0
    result = []
    x = 0
    while len(result) < 2:
        value = get(x, y)
        if value != prev:
            result.append(y / x)
            n_switches += 1
        x += 1
        prev = value
    return result

def find_approximate_answer(m1, m2, n=100):
    """got this by doing the math on paper"""
    x = n * (m2 + 1) / (m1 - m2)
    y = m2 * (x + 100)
    return int(x), int(y)

n = 0
for x, y in itertools.product(range(50), repeat=2):
    n += get(x, y)

print('part one:', n)

SEARCH = 20
m1, m2 = find_approximate_slopes(10000)
print('m1, m2:', m1, m2)
x_hat, y_hat = find_approximate_answer(m1, m2)
print('~x, ~y:', x_hat, y_hat)
fits = []
print('searching {} <= y < {}, {} <= x < {}'.format(y_hat - SEARCH, y_hat + SEARCH, x_hat - SEARCH, x_hat + SEARCH))
for y0 in range(y_hat - SEARCH, y_hat + SEARCH):
    for x0 in range(x_hat - SEARCH, x_hat + SEARCH):
        if all(get(x0 + x, y0 + y) for x, y in itertools.product(range(100), repeat=2)):
            fits.append((math.sqrt(x0**2 + y0**2), (x0, y0)))

print('found fits:', len(fits))
fits.sort()

d, (x, y) = fits[0]
answer = x * 10000 + y
print('part two:', '{:.2f}'.format(d), x, y, answer)

