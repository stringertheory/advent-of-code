"""first star in 18:23, second in 25:46

needed 11:12, 15:57 to place
"""
import pprint
import itertools
import math
import collections
import datetime
import utils
from termcolor import colored

# import networkx as nx
# from boltons import iterutils
# import traces
# from dateutil.parser import parse as date_parse

# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# itertools.combinations(abc, 2) -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4)) -> 4! possible orderings

# with open('input.txt') as infile:
#     s = infile.read().strip()

# for line in utils.iterstrip():
#     # print([line])
#     pass


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
                self.set(p1, inputs.pop(0), m1)
                self.index += 2
            elif opcode == 4:
                p1 = self.code[self.index + 1]
                v1 = self.get(p1, m1)
                self.index += 2
                print('output: ', v1)
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

class Robot:

    def __init__(self, filename):
        self.code = Intcode(filename)
        self.dir_point = 0
        self.directions = ['up', 'left', 'down', 'right']
        self.direction = 'up'
        self.x = 0
        self.y = 0
        self.n_painted = collections.Counter()
        self.colors = {}

    def get_color(self):
        return self.colors.get((self.x, self.y), 0)

    def paint(self, color):
        self.colors[(self.x, self.y)] = color
        self.n_painted[(self.x, self.y)] += 1
    
    def turn(self, left_or_right):
        if left_or_right == 0:
            self.dir_point -= 1
        elif left_or_right == 1:
            self.dir_point += 1
        self.direction = self.directions[self.dir_point % 4]
        
    def move(self):
        if self.direction == 'up':
            self.y += 1
        elif self.direction == 'left':
            self.x -= 1
        elif self.direction == 'down':
            self.y -= 1
        elif self.direction == 'right':
            self.x += 1
        else:
            raise 'wut'

    def run(self):
        color = 1
        while True:
            to_paint = self.code.run([color])
            turn_dir = self.code.run([])
            self.paint(to_paint)
            self.turn(turn_dir)
            self.move()
            color = self.get_color()

def printmatrix(layer):
    mapping = {
        'X': 'blue',
        ' ': 'white',
    }
    for row in layer:
        for value in row:
            print(colored('█', mapping[value]), end='')
        print()
            
r = Robot('input-11.txt')
try:
    r.run()
except StopIteration:
    pass

print(min(x for (x, y) in r.colors))
print(max(x for (x, y) in r.colors))
print(min(y for (x, y) in r.colors))
print(max(y for (x, y) in r.colors))

canvas = [[' ' for _ in range(43)] for _ in range(6)]

for (x, y), c in r.colors.items():
    if c == 0:
        canvas[-y][-x] = 'X'

printmatrix(canvas)
