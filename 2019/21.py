import sys
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
    

def generate_all_programs(n_lines):

    operations = ['AND', 'OR', 'NOT']
    first = ['A', 'B', 'C', 'D', 'T', 'J']
    second = ['T', 'J']
    
    if not n_lines:
        return [[]]
    
    result = []
    for first_part in itertools.product(operations, first, second):
        for rest in generate_all_programs(n_lines - 1):
            program = [first_part] + rest
            result.append(program)
                
    return result

def test(pattern, program):

    lines = program.strip().splitlines()
    last = lines.pop(-1)
    if last == 'WALK':
        assert len(pattern) == len('ABCD')
    elif last == 'RUN':
        assert len(pattern) == len('ABCDEFGHI')
    else:
        raise ValueError('last line must be RUN or WALK, got `{}`'.format(last))

    lookup = dict(zip('ABCDEFGHI', [i == '#' for i in pattern]))
    lookup['T'] = False
    lookup['J'] = False

    print('T', 'J')
    for line in lines:
        print(int(lookup['T']), int(lookup['J']), line)
        op, a, b = line.split()
        assert b in {'T', 'J'}
        if op == 'NOT':
            lookup[b] = (not lookup[a])
        elif op == 'OR':
            lookup[b] = (lookup[a] or lookup[b])
        elif op == 'AND':
            lookup[b] = (lookup[a] and lookup[b])
        else:
            raise ValueError('Invalid operation `{}`'.format(op))

    print(int(lookup['T']), int(lookup['J']))
    print()
    return lookup
            

def run_program(intcode, program):

    print(program)

    inputs = []
    for line in program.strip().splitlines():
        inputs.extend([ord(c) for c in line])
        inputs.append(ord('\n'))

    while True:
        try:
            out = intcode.run(inputs)
        except StopIteration:
            intcode.reset()
            break
        else:
            try:
                asc = chr(out)
            except Exception:
                print('\n=== result', out, '===\n\n', file=sys.stderr)
                break
            else:
                print(asc, end='')

program_one = """
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""

##.#.##...####
# ABCDEFGHI

# ##.#.##..
# ABCDEFGHI

# ((NOT A) OR (NOT B) OR (NOT C)) AND (D)
# (NOT (A AND C)) AND (D)

# (NOT A OR NOT C) AND D

# ((NOT A) OR (NOT B) OR (NOT C)) AND (D) AND (NOT ((NOT E) AND (NOT H)))
# ((NOT A) OR (NOT C)) AND (D) AND (E OR H)
# (NOT (A AND C)) AND (D) AND (E OR H)

program_two = """NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
NOT T T
OR H T
AND T J
RUN
"""
# program = """
# NOT E T
# NOT H J
# AND T J
# NOT J J
# RUN
# """
# program = """
# RUN
# """
# test('##.#.##..', program)
# test('##.####..', program)
# test('##.#.###.', program)
# test('##.#####.', program)
#    'ABCDEFGHI'
test('##.##.##.', program_two)
test('#.##.#.##', program_two)
# raise 'STO'
def possible_patterns(n):
    result = []
    for i in range(2**n):
        binary = "{:0{width}b}".format(i, width=n)
        road = ''.join([int(i) and '#' or '.' for i in binary])
        possible = True
        for char, group in itertools.groupby(road):
            if char == '.' and len(list(group)) > 3:
                possible = False
                break
        if possible:
            result.append(road)
    return result

intcode = Intcode('input.txt')

run_program(intcode, program_one)

intcode.reset()

run_program(intcode, program_two)

# n = 4
# if program.strip().endswith('RUN'):
#     n = 9
# for road in possible_patterns(n):
#     result = test(road, program)
#     print(road, result['J'])
#     # ex = (not (result['A'] and result['C'])) and result['D']
#     ex = (not (result['A'] and result['C'])) and result['D'] and (result['E'] or result['H'])
#     # ex = (result['E'] or result['H'])
#     print('ABCDEFGHI')
#     print()
#     # if not ex == result['J']:
#     #     raise 'wut'

impossible = '.**.'
'#####.**.'
'     ....' #impossible
'   J*..#.'
'  J**.#..'
'  JJ*.##.'
#...#...#...#

####.#.##...####
####.#.#...#####

# #####...#######
#     ABCDE
J = False
T = True
J = True
T = True
J = True
T = False
J = True

# ......x....x.....
# .....x.x..x.x....
# ....x...xx...x...
# #####.#.##...####
#    ABCDEFGHIJKLMNOP
# J = False
# T = False
# J = False
# T = True
# J = True
# T = True
# J = False

# ......x....x.....
# .....x.x..x.x....
# ....x...xx...x...
# #####.#.##...####
#      ABCDEFGHIJKLMNOP
# J = True
# T = False
# J = True
# T = True
# J = True
# T = True
# J = True


# n_lines = 0
# while True:
#     n_lines += 1
#     for lines in generate_all_programs(n_lines):
#         jumps = set(s for (o, f, s) in lines)
#         if 'J' in jumps:
#             program = '\n'.join(' '.join(i) for i in lines)
#             program += '\nWALK\n'

#             program = """NOT A J
# NOT B T
# OR T J
# NOT C T
# OR T J
# AND D J
# """
#             print(program)
#             inputs = []
#             for line in program.splitlines():
#                 inputs.extend([ord(c) for c in line])
#                 inputs.append(ord('\n'))

#             print(inputs)
                
#             while True:
#                 try:
#                     out = intcode.run(inputs)
#                 except StopIteration:
#                     intcode.reset()
#                     break
#                 else:
#                     try:
#                         asc = chr(out)
#                     except Exception:
#                         print('part one', out)
#                         raise
#                     else:
#                         print(asc, end='')
#                         if asc == 'D':
#                             print('\nreset\n')
#                             intcode.reset()
#                             break
    
#     print('finished all {} line programs'.format(n_lines))

# """
# ...
# ..#
# .#.
# .##
# #..
# #.#
# ##.
# ###

# NOT A J
# #...#...#...#...#..#.
# J   J   J   J   J   X

# .....x..
# ....x.x.
# ...x...x
# ####...#
#     ABCD

# ?
#     x
#    x x
#   x   x
# ####..#.
#    ABCD

#      x
#     x x
#    x   x
# ####.#.#

#      x
#     x x
#    x   x
# ####.##.#

#    x   x
#   x x x x
#  x   x   x
# ####.#..##

#          T  J
# NOT A J  0  1
# NOT B T  
# AND T J
# AND D J
# WALK

# ((NOT A) OR (NOT B) OR (NOT C)) AND (D AND E)

# NOT A J
# NOT B T
# OR T J
# NOT C T
# OR T J
# AND D J

# #...#.
# #...##

# #..##.
# #..###

# #.#.#.
# #.#.##

# #.###.
# #.####

# ##..#.
# ##..##

# ##.##.
# ##.###

# ###.#.
# ###.##

# #####.
# ######


# NOT A T
# OR B T


# """
