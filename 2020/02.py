import itertools
import collections

import utils

for key, group in itertools.groupby('aa12cd', key=lambda x: x.isdigit()):
    print(key, list(group))
for key, group in itertools.groupby('aa12cd'):
    print(key, list(group))

def valid_password_one(password, low, high, letter):
    counter = collections.Counter(password)
    return low <= counter[letter] <= high

def valid_password_two(password, low, high, letter):
    n = 0
    n += int(password[low - 1] == letter)
    n += int(password[high - 1] == letter)
    return n == 1

def has_atleast_n_consecutive(password, n=2):
    for key, group in itertools.groupby(password):
        if len(list(group)) >= n:
            return True

def has_exactly_n_consecutive(password, n=2):
    for key, group in itertools.groupby(password):
        if len(list(group)) == n:
            return True
        
def never_decrease(i):
    prev = -1
    for i in str(i):
        if int(i) < int(prev):
            return False
        prev = int(i)
    return True
        
count_one = 0
count_two = 0
for line in utils.iterstrip('input-02.txt'):
    policy, password = line.strip().split(': ')
    low, high = [int(_) for _ in policy.split()[0].split('-')]
    letter = policy.split()[1].strip()
    if valid_password_one(password, low, high, letter):
        count_one += 1
    if valid_password_two(password, low, high, letter):
        count_two += 1
print(count_one)
print(count_two)
    
