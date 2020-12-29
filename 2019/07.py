"""did both stars in 54:01"""

import pprint
import itertools
import math
import collections
import datetime
import utils

# import networkx as nx
# from boltons import iterutils
# import traces
# from dateutil.parser import parse as date_parse

# iterutils.chunked(range(10), 3) -> [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# iterutils.windowed(range(4), 3)) -> [(0, 1, 2), (1, 2, 3)]

# itertools.groupby('aa12cc', key=lambda x: x.isdigit())
# itertools.combinations(abc, 2) -> [(a, b), (a, c), (b, c)]
# itertools.permutations(range(4)) -> 4! possible orderings

import itertools
import math
import collections
import sys
import os
import pprint
import datetime

# import networkx as nx
# import boltons
# import sortedcontainers
# import traces

import utils


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

        self.index = 0
            
    def get(self, parameter, mode):
        if mode == 0:
            return self.code[parameter]
        elif mode == 1:
            return parameter
        else:
            raise 'wut get mode'

    def set(self, parameter, value, mode):
        if mode == 0:
            self.code[parameter] = value
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
            elif opcode == 99:
                raise StopIteration
            else:
                msg = 'wut opcode `{}`'.format(opcode)
                raise Exception(msg)
        return outputs

class Amp:

    def __init__(self, name, code_filename, phase_setting):
        self.phase_setting = phase_setting
        self.name = name
        self.code = Intcode(code_filename)
        self.first = True
        self.result = None

    def set_inout(self, in_amp, out_amp):
        self.in_amp = in_amp
        self.out_amp = out_amp

    def run(self, more_input=[]):
        
        if self.first:
            inputs = [self.phase_setting] + more_input
        else:
            inputs = more_input
        #print(self.name, self.first, inputs)

        self.first = False
        try:
            output = self.code.run(inputs)
        except StopIteration:
            self.result = inputs[0]
        else:
            self.out_amp.run([output])

        return self.result
            
code_filename = 'input-07.txt'

phase_sequence = [9, 8, 7, 6, 5]
results = []
for phase_sequence in itertools.permutations([5, 6, 7, 8, 9]):

    A = Amp('A', code_filename, phase_sequence[0])
    B = Amp('B', code_filename, phase_sequence[1])
    C = Amp('C', code_filename, phase_sequence[2])
    D = Amp('D', code_filename, phase_sequence[3])
    E = Amp('E', code_filename, phase_sequence[4])

    A.set_inout(E, B)
    B.set_inout(A, C)
    C.set_inout(B, D)
    D.set_inout(C, E)
    E.set_inout(D, A)

    b = A.run([0])
    results.append((b, phase_sequence))

# results = []
# for phase_sequence in itertools.permutations([5, 6, 7, 8, 9]):

#     output = 0
#     for phase_setting in phase_sequence:    
#         outputs = comp.run([phase_setting, output])
#         output = outputs[0]
            
#     results.append((output, phase_sequence))

for i in sorted(results):
    print(i)
