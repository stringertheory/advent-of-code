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
        
    def run(self):
        index = 0
        while True:
            instruction = '{:05d}'.format(self.code[index])
            opcode = int(instruction[-2:])
            m1 = int(instruction[-3])
            m2 = int(instruction[-4])
            m3 = int(instruction[-5])
            if opcode == 1:
                p1, p2, p3 = self.code[(index + 1):(index + 4)]
                v1 = self.get(p1, m1)
                v2 = self.get(p2, m2)
                self.set(p3, v1 + v2, m3)
                index += 4
            elif opcode == 2:
                p1, p2, p3 = self.code[(index + 1):(index + 4)]
                v1 = self.get(p1, m1)
                v2 = self.get(p2, m2)
                self.set(p3, v1 * v2, m3)
                index += 4
            elif opcode == 3:
                p1 = self.code[index + 1]
                self.set(p1, int(input('input: ')), m1)
                index += 2
            elif opcode == 4:
                p1 = self.code[index + 1]
                v1 = self.get(p1, m1)
                index += 2
                print('output: ', v1)
            elif opcode == 5:
                p1 = self.code[index + 1]
                p2 = self.code[index + 2]
                if self.get(p1, m1):
                    index = self.get(p2, m2)
                else:
                    index += 3
            elif opcode == 6:
                p1 = self.code[index + 1]
                p2 = self.code[index + 2]
                if not self.get(p1, m1):
                    index = self.get(p2, m2)
                else:
                    index += 3
            elif opcode == 7:
                p1, p2, p3 = self.code[(index + 1):(index + 4)]
                self.set(p3, int(self.get(p1, m1) < self.get(p2, m2)), m3)
                index += 4
            elif opcode == 8:
                p1, p2, p3 = self.code[(index + 1):(index + 4)]
                self.set(p3, int(self.get(p1, m1) == self.get(p2, m2)), m3)
                index += 4
            elif opcode == 99:
                print('halt')
                break
            else:
                msg = 'wut opcode `{}`'.format(opcode)
                raise Exception(msg)
                
a = Intcode('input-05.txt')
a.run()
            
