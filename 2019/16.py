"""start at 4:32:45
first at 4:46
second at  SHEEEEEEE
"""
import sys
import copy
import pprint
import itertools
import math
import collections
import datetime
import utils
import numpy as np
from scipy import sparse

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def make_pattern(n_repeat, base_pattern):
    result = []
    for i in base_pattern:
        result.extend(n_repeat * [i])
    result.append(result.pop(0))
    return result

def make_pattern_sparse(n_repeat, base_pattern):
    result = {}
    for index, i in enumerate(make_pattern(n_repeat, base_pattern)):
        if i:
            result[index] = i
    return result

def compute_row(signal, base, n_repeat, multi):
    pattern = make_pattern(n_repeat, base)
    subsignal_length = int((len(signal) / multi))
    subsignal = signal
    beat = min(len(signal), len(pattern) * subsignal_length)
    beat2 = min(len(signal), lcm(len(pattern), subsignal_length))
    # print('go', multi, len(signal), subsignal_length)
    # print(base, n_repeat, len(pattern))
    # print(beat)

    # for i in range(len(signal)):
    #     print('{:2d}'.format(signal[i]), end='')
    # print()
    # for i in range(len(signal)):
    #     print('{:2d}'.format(pattern[i % len(pattern)]), end='')
    # print()
    # for i in range(len(signal)):
    #     print('{:2d}'.format(signal[i] * pattern[i % len(pattern)]), end='')
    # print()

    # for i in range(beat):
    #     print('{:2d}'.format(signal[i]), end='')
    # print()
    # for i in range(beat):
    #     print('{:2d}'.format(pattern[i % len(pattern)]), end='')
    # print()
    # for i in range(beat):
    #     print('{:2d}'.format(signal[i] * pattern[i % len(pattern)]), end='')
    # print()
    
    s = 0
    for i in range(beat2):
        s += signal[i] * pattern[i % len(pattern)]

    n_beats = len(signal) / beat2
    n_full_beats = int(n_beats)
    offset = n_full_beats * beat2

    extra_s = 0
    for i in range(offset, len(signal)):
        # print(i, signal[i], pattern[i % len(pattern)])
        extra_s += signal[i] * pattern[i % len(pattern)]

    print(n_repeat, beat, beat2, offset, s, s * n_full_beats, n_beats, n_full_beats, extra_s, s * n_full_beats + extra_s)
    result = s * n_full_beats + extra_s
    return result

with open('input-16.txt') as infile:
    s = infile.read().strip()

base = [0, 1, 0, -1]
          
signal = [int(i) for i in s]
# signal = [int(i) for i in '12345678']
# signal = [int(i) for i in '03036732577212944063491565474664']
# signal = [int(i) for i in '02935109699940807407585447034323']

def part_one(signal, n_phases):
    signal = signal
    for phase_n in range(n_phases):
        output = []
        for n_repeat, _ in enumerate(signal, 1):
            pattern = make_pattern(n_repeat, base)
            s = 0
            for index, element in enumerate(signal):
                s += element * pattern[index % len(pattern)]
            s_last = int(str(s)[-1])
            output.append(s_last)
        signal = output
    return signal

new_signal = part_one(signal, 100)
print('one', ''.join(str(_) for _ in new_signal[:8]))

def part_two(signal, mult, n_phases):

    signal = signal * mult
    message_offset = int(''.join(str(_) for _ in signal[:7]))
    n_tail = len(signal) - message_offset
    
    for phase_n in range(100):
        new_signal = [None for _ in range(n_tail)]
        new_signal[-1] = signal[-1]
        for i in range(1, n_tail):
            new_signal[-(i + 1)] = abs(new_signal[-i] + signal[-(i + 1)]) % 10
        signal = new_signal

    return signal

signal_tail = part_two(signal, 10000, 100)

print('two', ''.join(str(_) for _ in signal_tail[:8]))

# # matrix_sparse = sparse.csr_matrix((len(signal), len(signal)))
# # print(matrix_sparse.toarray())
# # for n_repeat, _ in enumerate(signal, 1):
# #     y = n_repeat - 1
# #     pattern = make_pattern(n_repeat, base)
# #     for x, element in enumerate(signal):
# #         matrix_sparse[y, x] = pattern[x % len(pattern)]

# # print(matrix_sparse.toarray())

# for x, v in enumerate(signal):
#     n = '{:2d}'.format(v)
#     print(n, end=' ')
# print()

# for y in range(len(signal)):
#     s = 0
#     for x, v in enumerate(signal):
#         q = get_matrix_value(y, x, base)
#         s += v * q
#         if q:
#             n = '{:2d}'.format(q)
#         else:
#             n = '  '
#         print(n, end=' ')
#     print('{:4d}'.format(s), abs(s) % 10)

# raise 'STOP'

# signal = np.array([signal])
# print(signal)
# for i in range(4):
#     sums = matrix_sparse.dot(signal.T).sum(axis=1)
#     signal = np.array([abs(sums) % 10])
#     print(signal)
    
# raise 'STOP'
    
# print(''.join(str(_) for _ in signal[0:8]))
# print(''.join(str(_) for _ in signal[message_offset:message_offset+8]))

# print()

# # for phase_n in range(4):
# #     # print('phase # {}'.format(phase_n + 1), file=sys.stderr)
# #     print(''.join(str(_) for _ in signal))
# #     output = []
# #     for n_repeat in range(1, len(signal) + 1):
# #         output.append(compute_row(signal, base, n_repeat, mult))
# #         if n_repeat > 3:
# #             raise 'ST'
# #     signal = output
        
# # print(''.join(str(_) for _ in signal[0:8]))
# # print(''.join(str(_) for _ in signal[message_offset:message_offset+8]))

