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
                try:
                    val = inputs.pop(0)
                except IndexError:
                    command = input('').strip()
                    inputs = []
                    for line in command.strip().splitlines():
                        inputs.extend([ord(c) for c in line])
                        inputs.append(ord('\n'))
                    val = inputs.pop(0)
                self.set(p1, val, m1)
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
    
def parse_output(output):
    result = {
        'name': None,
        'doors': [],
        'items': [],
    }
    reading_direction = False
    reading_items = False
    for line in output.splitlines():
        if line.startswith('== '):
            result['name'] = line.split('==')[1].strip()
        elif line.startswith('Doors here lead'):
            reading_direction = True
        elif line.startswith('Items here'):
            reading_items = True
        elif reading_direction:
            if line.startswith('-'):
                direction = line.strip().split()[-1]
                result['doors'].append(direction)
            else:
                reading_direction = False
        elif reading_items:
            if line.startswith('-'):
                item = line[2:].strip()
                result['items'].append(item)
            else:
                reading_direction = False
    
    return result

def all_combos(iterable):
    n = len(iterable)
    result = set()
    for i in range(1, n + 1):
        for c in itertools.combinations(list(iterable), i):
            result.add(tuple(sorted(c)))
    return list(sorted(result))

dd = {
    'north': ( 0, -1),
    'south': ( 0,  1),
    'west':  ( 1,  0),
    'east':  (-1,  0),
}
            
i = Intcode('input-25.txt')

dont_take = {
    'infinite loop',
    'giant electromagnet',
    'escape pod',
    'photons',
    'molten lava',
}
indiana_jonesin = False
tried_combos = set()
inventory = set()
i.graph = nx.Graph()
x, y = 0, 0
output_chars = []
inputs = []
while True:
    try:
        out = i.run(inputs)
    except StopIteration:
        i.reset()
        output = ''.join(output_chars)
        print(output)
        break
    else:
        asc = chr(out)
        output_chars.append(asc)
        if asc == '?':

            output = ''.join(output_chars)
            output_chars = []
            parsed = parse_output(output)

            pprint.pprint(parsed)
            print('inventory', inventory)
            print(output, end=' ')
            sys.stdout.flush()

            inputs = []
            command = None
            if not indiana_jonesin and parsed['name'] == 'Security Checkpoint' and len(inventory) == 8:
                indiana_jonesin = True
                untried_combos = all_combos(inventory)
                print('=' * 400, 'INDIANA JONESIN', len(untried_combos))

            combo = tuple(sorted(inventory))
            if indiana_jonesin:
                if combo in untried_combos:
                    command = 'south'
                    untried_combos.remove(combo)
                    print('n remaining', combo, len(untried_combos))
                else:
                    next_try = untried_combos[0]
                    print('next try', next_try)
                    to_take = set(next_try).difference(combo)
                    to_drop = set(combo).difference(next_try)
                    if to_take:
                        item = to_take.pop()
                        command = 'take {}'.format(item)
                        inventory.add(item)
                    elif to_drop:
                        item = to_drop.pop()
                        command = 'drop {}'.format(item)
                        inventory.remove(item)
                    else:
                        raise 'wut'
                    print('jonesin', command)
                    
            if not command and parsed['items']:
                item = random.choice(parsed['items']).strip()
                if item not in dont_take:
                    command = 'take {}'.format(item)
                    inventory.add(item)
            
            if not command and parsed['doors']:
                command = random.choice(parsed['doors']).strip()

            if command:
                inputs = [ord(c) for c in command]
                inputs.append(ord('\n'))
                

