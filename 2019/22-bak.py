import random
import math
import collections
import utils
from termcolor import colored

def print_deck(deck):
    # print(''.join('{:3d}'.format(i) for i in range(len(deck))))
    print(' '.join('{:2d}'.format(i) for i in list(deck)[:30]))

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
    print('deck new:')
    print_deck(result)
    return result

def deal_into_new_stack_index(deck_size, index):
    result = (deck_size - index - 1) % deck_size
    print('new', index, result)
    return result

def cut(deck, n):
    temp = list(deck)
    result = collections.deque(temp[n:] + temp[:n])
    print('deck cut {}:'.format(n))
    print_deck(result)
    return result

def cut_index(deck_size, n, index):
    result = (index + n) % deck_size
    print('cut', n, index, result)
    return result

def deal_with_increment(deck, n):
    index = 0
    result = collections.deque(None for card in deck)
    while deck:
        result[index % len(result)] = deck.popleft()
        index += n
    print('deck inc {}:'.format(n))
    print_deck(result)
    return result

def deal_with_increment_index(deck_size, n, index, max_i=100000):
    print('start inc', deck_size, n, index)
    i = 0
    while True and i < max_i:
        t = n * i
        print(t, t % deck_size)
        if t % deck_size == 1:
            mult = i
            break
        i += 1

    if i >= max_i:
        raise ValueError('hit max iterations')
        
    result = (index * mult) % deck_size
    print('inc', n, index, mult, result)
    return result

def main():

    N = 10007#119315717514047
    # deck = collections.deque(range(N))

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

    lines = []
    for line in utils.iterstrip('input.txt'):
        lines.append(line)
        
    # print_deck(deck)
    # for line in lines:
    #     deck = one_shuffle(deck, line)

    index = 2020
    for line in reversed(lines):
        index = one_shuffle_index(N, line, index)

    print(index)
        
    # print(cut_index(len(deck), 10, 7))
    
    # deck = cut(deck, 10)

    # # print_deck(deck)
    # print(deck[7])
    raise 'STOP'
        
    # random.shuffle(lines)
        
    for line in lines:
        index = one_shuffle_index(DECK_SIZE, line, index)
        deck = one_shuffle(deck, line)

    print(deck.index(2019))
    print(deck[2020], index)
    
    # # deck = deal_into_new_stack(deck)
    # # index = deal_into_new_stack_index(DECK_SIZE, 2020)
    # # deck = cut(deck, 3)
    # # index = cut_index(DECK_SIZE, 3, 2020)

    # # print(deck[2020], index)
    # # raise 'STOP'

    # q = 20
    # b = 2
    # print(deck)
    # # print()
    # print([deal_with_increment_index(N, q, i) for i in range(N)])
    # deck = deal_with_increment(deck, q)
    # index = deal_with_increment_index(DECK_SIZE, q, b)

    # # print()
    # print(deck)
    # if deck[b] == index:
    #     print(colored(deck[b], 'green'))
    # else:
    #     print(colored(deck[b], 'red'), end=' != ')
    #     print(colored(index, 'red'))
        
    # print(deck[b] == index)

    # # deck[q] = deck[1]
    # # deck[5] = deck[(40) % N] = 1
    
    # print(N / q, N // q, N % q)
    # print('ceil', math.ceil(N / q))
    # print((N + 1) / q, (N + 1) // q, (N + 1) % q)
    # print(N, q)
    
    # print((N - 1) // q, (N - 1) % q)

        
main()


    
