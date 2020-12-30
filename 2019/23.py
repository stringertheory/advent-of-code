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
        nwait = 0
        while True:
            instruction = '{:05d}'.format(self.code[self.index])
            opcode = int(instruction[-2:])
            m1 = int(instruction[-3])
            m2 = int(instruction[-4])
            m3 = int(instruction[-5])
            # print(self.index, instruction, opcode, m1, m2, m3)
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
                # self.set(p1, val, m1)
                try:
                    val = inputs.pop(0)
                except IndexError:
                    nwait += 1
                    # print('input -1:', self.nic, nwait)
                    val = -1
                self.set(p1, val, m1)
                self.index += 2
                if val == -1:
                    return 'input', None
            elif opcode == 4:
                p1 = self.code[self.index + 1]
                v1 = self.get(p1, m1)
                self.index += 2
                # print('output: ', v1)
                return 'output', v1
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
    
class Packet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NIC:
    def __init__(self, address, filename):
        self.address = address
        self.program = Intcode(filename)
        self.program.nic = self
        self.packets = []
        self.n_inputs = 0

    def __repr__(self):
        return '<NIC {}>'.format(self.address)
    
    def run(self):
        outgoing = []
        while True:
            try:
                out_type, out = self.program.run(self.packets)
            except StopIteration:
                raise
            else:
                if out_type == 'output':
                    self.n_inputs = 0
                    outgoing.append(out)
                    if len(outgoing) == 3:
                        # print(self.address, outgoing)
                        yield outgoing
                        outgoing = []
                elif out_type == 'input':
                    # print('input -1')
                    self.n_inputs += 1
                    return
                else:
                    raise 'wut is out_type=`{}`'.format(out_type)

N = 50

nics = {}
for i in range(N):
    nics[i] = NIC(i, 'input-23.txt')
    nics[i].program.run([i])

part1_done = False
natx = None
naty = None
previous_natx = None
previous_naty = None
    
nic_no = 0
while True:
    nic = nics[nic_no]
    for address, x, y in nic.run():
        print(nic_no, address, x, y)
        if address == 255:
            if not part1_done:
                print('part 1 = {}'.format(y), file=sys.stderr)
                part1_done = True
            print('NAT received', x, y)
            natx, naty = x, y
        else:
            nics[address].packets.extend([x, y])

    nic_no += 1
    nic_no = nic_no % N

    if nic_no == 0:
        idle = all(nic.n_inputs > 1 for nic in nics.values())
        if idle:
            print('idle')
            if naty == previous_naty:
                print('part 2 = {}'.format(naty), file=sys.stderr)
                sys.exit()
            nics[0].packets.extend([natx, naty])
            # print('NATS', NATS, nics[0].packets)
            previous_natx = natx
            previous_naty = naty
    
    
