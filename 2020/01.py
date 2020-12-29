import itertools
import math

import utils

def read_input(filename='input.txt'):
    return [int(line) for line in utils.iterstrip(filename)]

def solve(numbers, n):
    for index, items in enumerate(itertools.combinations(numbers, n)):
        if sum(items) == 2020:
            print(items, math.prod(items))
    print(index)

numbers = read_input('input-01.txt')
solve(numbers, 2)
solve(numbers, 3)
