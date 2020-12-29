"""starting at 5:30"""
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
                # val = input('which way? ').strip().lower()
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


def print_squares(m, dead, start, end):
    xs = [x for x, y in m.keys()]
    ys = [y for x, y in m.keys()]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    board = []
    for y in range(y_min, y_max + 1):
        row = []
        for x in range(x_min, x_max + 1):
            char = m.get((x, y), ' ')
            if (x, y) == start:
                char = 'o'
            elif (x, y) == end:
                char = 'x'
            if (x, y) in dead:
                char = colored(char, 'red')
                
            row.append(char)
        board.append(row)

    for row in board:
        print(''.join(row))
    print()
    
i = Intcode('input-15.txt')

def find_unexplored_neighbors(position, squares):
    result = []
    x, y = position
    if (x, y + 1) not in squares:
        result.append(1)
    if (x, y - 1) not in squares:
        result.append(2)
    if (x - 1, y) not in squares:
        result.append(3)
    if (x + 1, y) not in squares:
        result.append(4)
    return result

def find_undead_neighbors(position, dead):
    return find_unexplored_neighbors(position, dead)



index = 0
start = (0, 0)
end = None
graph = nx.Graph()
value = 1
position = (0, 0)
exploring = (0, 0)

squares = {}
dead = set()
squares[start] = '.'
while True:
    try:
        out = i.run([value])
    except StopIteration:
        break
    else:
        index += 1

        x, y = position
        if value == 1:
            neighbor = (x, y + 1)
        elif value == 2:
            neighbor = (x, y - 1)
        elif value == 3:
            neighbor = (x - 1, y)
        elif value == 4:
            neighbor = (x + 1, y)
        else:
            raise 'wut'
        
        if out == 0:
            squares[neighbor] = '#'
            dead.add(neighbor)
            
        elif out == 1 or out == 2:
            position = neighbor
            squares[position] = '.'
            graph.add_edge((x, y), position)
            if out == 2:
                end = position
        else:
            raise 'wut'

        # print_squares(squares, dead, start, end)
        # print('position', position)
        
        unexplored_neighbors = find_unexplored_neighbors(position, squares)
        # print('unexplored', unexplored_neighbors)
        if unexplored_neighbors:
            value = random.choice(unexplored_neighbors)
        else:
            undead_neighbors = find_undead_neighbors(position, dead)
            # print('undead', undead_neighbors)
            if not undead_neighbors:
                dead.add(position)
                print('completely explored!', index)
                break

            if len(undead_neighbors) == 1:
                dead.add(position)

            value = random.choice(undead_neighbors)
                
        # print('choice', value)
        # input()
        # time.sleep(0.005)
        
print_squares(squares, dead, start, end)

a = nx.shortest_path(graph, (0, 0), end)
print(len(a) - 1)

path_lengths = []
for target, path in nx.single_source_shortest_path(graph, end).items():
    path_lengths.append(len(path) - 1)

print(max(path_lengths))
