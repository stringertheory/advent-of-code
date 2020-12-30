"""started at 10:45:30, 2 stars at 12:15"""
import time
import random
import pprint
import itertools
import math
import collections
import datetime
import utils
from termcolor import colored


from boltons import iterutils

# from pynput.keyboard import Key, Listener

# def on_press(key):
#     print('{0} pressed'.format(
#         key))
#     return key

# def on_release(key):
#     print('{0} release'.format(
#         key))
#     return False

# # Collect events until released
# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     value = listener.join()
#     print(value)

# raise 'STOP'
    
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

chars = {
    0: ' ',
    1: '|',
    2: 'X',
    3: '_',
    4: 'O',
}
    
def draw(game):
    max_x = max(x for x, y in game.keys())
    max_y = max(y for x, y in game.keys())
    board = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            val = game.get((x, y), 0)
            row.append(chars[val])
        board.append(row)
    for row in board:
        print(''.join(row))

            
i = Intcode('input-13.txt')
i.code[0] = 2

outputs = []
input_value = 1
paddle_x = 0
paddle_y = 0
ball_x = 0
ball_y = 0
latest_score = 0
game = {}
while True:
    try:
        output = i.run([input_value])
    except StopIteration:
        break
    else:
        outputs.append(output)

        if not len(outputs) % 3:

            x, y, tile_id = outputs[-3:]
            if x == -1 and y == 0:
                latest_score = tile_id
            else:
                game[(x, y)] = tile_id
                
            if tile_id == 4:
                ball_x = x
                ball_y = y
            elif tile_id == 3:
                paddle_x = x
                paddle_y = y
                
            dx = ball_x - paddle_x
            dy = ball_y - paddle_y
            if dx > 0:
                input_value = 1
            elif dx < 0:
                input_value = -1
            else:
                if abs(dy) < 5:
                    input_value = 0
                else:
                    input_value = random.randint(-1, 1)

            draw(game)
            print('score:', latest_score)
            time.sleep(0.001)
        
            
