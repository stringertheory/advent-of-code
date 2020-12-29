"""starting at 9:28
first star at 9:40
second at 
"""
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
    
i = Intcode('input-17.txt')

filename = 'output-17.txt'
with open(filename, 'w') as outfile:
    index = 0
    while True:
        try:
            out = i.run([])
        except StopIteration:
            break
        else:
            index += 1
            output_value = chr(out)
            outfile.write(output_value)

start = None
board = []
for y, line in enumerate(utils.iterstrip(filename)):
    if line.strip():
        row = []
        for x, c in enumerate(line):
            row.append(int(c == '#' or c == '^'))
            if c == '^':
                start = (x, y)
        board.append(row)

def print_board(board, graph, current):
    for y, row in enumerate(board):
        this = []
        for x, c in enumerate(row):
            if c:
                if (x, y) == current:
                    this.append(colored('#', 'yellow'))
                elif graph.nodes[(x, y)].get('avoid'):
                    this.append(colored('#', 'red'))
                elif graph.nodes[(x, y)].get('marked'):
                    this.append(colored('#', 'green'))
                else:
                    this.append(colored('#', 'white'))
            else:
                this.append(' ')
        print(' '.join(this))
        
ints = []
for y, row in enumerate(board):
    for x, val in enumerate(row):
        if y == 0 or y == (len(board) - 1):
            continue
        if x == 0 or x == (len(row) - 1):
            continue
        t = board[y - 1][x]
        r = board[y][x + 1]
        b = board[y + 1][x]
        l = board[y][x - 1]
        if val and t and r and b and l:
            ints.append((x, y))

p1 = 0
for x, y in ints:
    p1 += x * y

print('part one', p1)

graph = nx.Graph()
for y, row in enumerate(board):
    for x, val in enumerate(row):
        if val:
            if (not y == 0) and board[y - 1][x]:
                graph.add_edge((x, y), (x, y - 1))
            if (not y == (len(board) - 1)) and board[y + 1][x]:
                graph.add_edge((x, y), (x, y + 1))
            if (not x == 0) and board[y][x - 1]:
                graph.add_edge((x, y), (x - 1, y))
            if (not x) == (len(row) - 1) and board[y][x + 1]:
                graph.add_edge((x, y), (x + 1, y))

# print(graph.edges)

# 01234
#   5 9
#   678
# start = (0, 0)
# graph = nx.Graph()
# graph.add_edge((0, 0), (1, 0))
# graph.add_edge((1, 0), (2, 0))
# graph.add_edge((2, 0), (3, 0))
# graph.add_edge((3, 0), (4, 0))
# graph.add_edge((2, 0), (2, 1))
# graph.add_edge((2, 1), (2, 2))
# graph.add_edge((2, 2), (3, 2))
# graph.add_edge((3, 2), (4, 2))
# graph.add_edge((4, 2), (4, 1))
# graph.add_edge((4, 1), (4, 0))

def path(board, g, start):
    print_board(board, g, start)
    t = nx.dfs_tree(g, start)
    branches = []
    result = []
    node = start
    while True:#not all(n.get('marked') for _, n in g.nodes.items()):
        # print_board(board, g, node)
        result.append(node)
        g.nodes[node]['marked'] = True
        unexplored = [n for n in g.neighbors(node) if not g.nodes[n].get('marked')]
        if not unexplored:
            if branches:
                last_branch = branches.pop()
            else:
                break
            result.extend(nx.shortest_path(g, node, last_branch)[1:])
            node = last_branch
        else:
            if len(unexplored) > 1:
                branches.append(node)
            node = unexplored.pop()

    prev = None
    dedupe = []
    for i in result:
        if i == prev:
            continue
        dedupe.append(i)
        prev = i

    return dedupe

def commands(path, start_orientation):

    turns = ['^', '>', 'v', '<']
    
    result = []
    orientation = start_orientation
    for a, b in iterutils.windowed(path, 2):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        if abs(dx) + abs(dy) != 1:
            print(a, b, dx, dy)
            raise 'wut'
        if dx == 1:
            move_orientation = '>'
        elif dx == -1:
            move_orientation = '<'
        elif dy == 1:
            move_orientation = 'v'
        elif dy == -1:
            move_orientation = '^'

        while orientation != move_orientation:
            # print(a, a, orientation, end=' ')
            orientation = turns[(turns.index(orientation) + 1) % len(turns)]
            # print(orientation)
            result.append('R')

        result.append(1)
        # print(a, b, orientation, move_orientation)


    counter = collections.Counter()
    path = ''.join(str(i) for i in result)
    for a in iterutils.windowed(path, 10):
        for b in iterutils.windowed(path, 9):
            counter[a] += 1

    # print(counter)
    # # print(path)
    # for l in range(2, 10):#int(len(path) / 2) + 1):
    #     for j in range(0, len(path) - l + 1):
    #         substring = path[j:(j + l)]
    #         print(substring, end=' ')
    #     print()
        
    for i, j in itertools.groupby(result):
        print(i, len(list(j)))
        
    raise 'STOP'

# traversal = path(board, graph, start)
# commands(traversal, '^')

# raise "STOP"

i = Intcode('input-17.txt')
i.code[0] = 2

print(ord('y'), ord('n'), ord('\n'))

# got this by printing out the maze...
answer = 'A,B,A,C,A,B,C,B,C,B\n'
A = 'R,5,5,R,5,5,R,6,R,4\n'
B = 'R,5,5,R,5,5,L,4\n'
C = 'R,4,L,4,L,5,5,L,5,5\n'

inputs = [ord(c) for c in answer]
inputs.extend([ord(c) for c in A])
inputs.extend([ord(c) for c in B])
inputs.extend([ord(c) for c in C])
inputs.extend([ord(c) for c in 'n\n'])

# inputs = [65, 44, 66, 44, 67, 10]
# inputs.extend([82, 44, ord('9'), 10])
# inputs.extend([ord('1'), 44, 82, 44, ord('2'), 44, ord('R'), 44, ord('4'), 10])
# inputs.extend([ord('0'), 10])
# inputs.extend([110, 10])

index = 0
while True:
    try:
        out = i.run(inputs)
    except StopIteration:
        break
    else:
        index += 1
        print(chr(out), end='')

print()
print(out)



# def path(board, g, start):
#     tree = nx.bfs_tree(g, start)
    
#     print_board(board, tree, start)
#     raise 'STOP'
#     result = []
#     to_visit = []
#     while not all(n.get('explored') for _, n in tree.nodes.items()):
#         node = to_visit.pop()
#         result.append(node)
#         tree.nodes[node]['explored'] = True
#         unexplored = [n for n in tree.neighbors(node) if not tree.nodes[n].get('explored')]
#         undead = [n for n in tree.neighbors(node) if not tree.nodes[n].get('avoid')]
#         if len(undead) == 1:
#             tre.nodes[node]['avoid'] = True
#         print(node, unexplored, undead)
#         print_board(board, graph, node)
#         if unexplored:
#             node = unexplored.pop()
#         else:
#             node = undead.pop()
#         input()
        
#     for node in g.nodes:
#         print(node, g.nodes[node].get('avoid'))
#     return result
