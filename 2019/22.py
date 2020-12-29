import random
import math
import collections
import utils
from termcolor import colored

def print_deck(deck, limit=10):
    # print(''.join('{:3d}'.format(i) for i in range(len(deck))))
    print(' '.join('{:2d}'.format(i) for i in list(deck)[:limit]))

def one_shuffle(deck, line):
    if line.startswith('deal with'):
        n = int(line.split()[-1])
        return deal_with_increment(deck, n)
    elif line.startswith('cut'):
        n = int(line.split()[-1])
        return cut(deck, n)
    elif line.startswith('deal into'):
        return deal_into_new_stack(deck)
    else:
        raise ValueError('invalid line `{}`'.format(line))
    
def one_shuffle_index(deck_size, line, index):
    if line.startswith('deal with'):
        n = int(line.split()[-1])
        return deal_with_increment_index(deck_size, n, index)
    elif line.startswith('cut'):
        n = int(line.split()[-1])
        return cut_index(deck_size, n, index)
    elif line.startswith('deal into'):
        return deal_into_new_stack_index(deck_size, index)
    else:
        raise ValueError('invalid line `{}`'.format(line))

def deal_into_new_stack(deck):
    result = collections.deque(reversed(deck))
    # print('deck new:')
    # print_deck(result)
    return result

def deal_into_new_stack_index(deck_size, index):
    result = (deck_size - index - 1) % deck_size
    # print('new', index, result)
    return result

def cut(deck, n):
    temp = list(deck)
    result = collections.deque(temp[n:] + temp[:n])
    # print('deck cut {}:'.format(n))
    # print_deck(result)
    return result

def cut_index(deck_size, n, index):
    result = (index + n) % deck_size
    # print('cut', n, index, result)
    return result

def deal_with_increment(deck, n):
    index = 0
    result = collections.deque(None for card in deck)
    while deck:
        result[index % len(result)] = deck.popleft()
        index += n
    # print('deck inc {}:'.format(n))
    # print_deck(result)
    return result

def deal_with_increment_index(deck_size, n, index, max_i=100000):
    # print('start inc', deck_size, n, index)
    i = 0
    while True and i < max_i:
        t = 1 + deck_size * i
        if t % n == 0:
            mult = t // n
            break
        i += 1

    if i >= max_i:
        raise ValueError('hit max iterations')
        
    result = (index * mult) % deck_size
    # print('inc', n, index, mult, result)
    return result

def f(i, t, a, b, n):
    """
    a * (1 - p) // (1 - b) + i * p, where p = pow(b, t)

    (a + b) % c = (a % c + b % c) % c
    (a * b) % c = (a % c * b % c) % c
    """
    # p = pow(b, t)
    # A = a * (1 - p) // (1 - b)
    # B = i * p
    # Amod = (a * (1 - p) // (1 - b)) % n
    Amod1 = a % n
    # Amod2 = ((1 - p) // (1 - b)) % n
    Amod2a = (1 % n - pow(b, t, n)) % n
    Amod2b = pow(1 - b, -1, n)
    Amod2 = (Amod2a * Amod2b) % n
    Amod = (Amod1 * Amod2) % n
    Bmod = (i % n * pow(b, t, n)) % n
    # result = (A + B) % n
    result = (Amod + Bmod) % n
    return result

def main():

    # N = 10007#119315717514047
    N = 119315717514047
    # N_SHUFFLE = 3 * 10006
    N_SHUFFLE = 101741582076661

    print(N_SHUFFLE < N)
    
    lines = []
    for line in utils.iterstrip('input-22.txt'):
        lines.append(line)

    # deck = collections.deque(range(N))
    # for line in lines:
    #     deck = one_shuffle(deck, line)
    # print_deck(deck)

    # use first two elements to get the slope and intercept
    index = 0
    for line in reversed(lines):
        index = one_shuffle_index(N, line, index)
    a = index

    index = 1
    for line in reversed(lines):
        index = one_shuffle_index(N, line, index)
    b = index - a

    print(a, b)
    print(pow(1 - b, -1, mod=N))
    
    # test by looking at one deck after one shuffle
    for x in range(10):
        index = x
        for line in reversed(lines):
            index = one_shuffle_index(N, line, index)
        print(x, index, (a + x * b) % N, index == (a + x * b) % N)

    print()

    # test by looking at one index over several shuffles
    index = 2020
    for t in range(1, 10):
        for line in reversed(lines):
            index = one_shuffle_index(N, line, index)
        print(t, index, f(2020, t, a, b, N), index == f(2020, t, a, b, N))

    print()

    # I THINK THIS IS RIGHT BUT HOW TO COMPUTE!!!
    print(f(2020, N_SHUFFLE, a, b, N))

    # def g(i, a, b, n):
    #     return (a + i * b) % n
    
    # print(g(2020, a, b, N))
    # print(g(g(2020, a, b, N), a, b, N))
    # print(g(g(g(2020, a, b, N), a, b, N), a, b, N))

    # print_deck(deck)
    # deck = cut(deck, 2)
    # deck = deal_into_new_stack(deck)
    # deck = deal_with_increment(deck, 3)

    # f = cut_index(N, 2, deal_into_new_stack_index(N, deal_with_increment_index(N, 3, 7)))

    # bunga = deal_with_increment_index(N, 3, 7)
    # bunga = deal_into_new_stack_index(N, bunga)
    # bunga = cut_index(N, 2, bunga)
    
    # print(f, bunga)
    # shee = [(11 - 7*i)%10 for i in range(10)]
    # print_deck(shee)
    # shee = [(1 - 7*i)%10 for i in range(10)]
    # print_deck(shee)
    # # print((11 - 7*7) % 10)
    
    # raise 'STOP'
    
main()


    
