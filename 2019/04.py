import itertools

def has_two(i):
    prev = None
    for i in str(i):
        if i == prev:
            return True
        prev = i

def has_pair(i):
    for k, g in itertools.groupby(str(i)):
        if len(list(g)) == 2:
            return True
        
def never_decrease(i):

    prev = -1
    for i in str(i):
        if int(i) < int(prev):
            return False
        prev = int(i)

    return True

def valid(i):
    a = has_pair(i)
    b = never_decrease(i)
    return a and b

s = 0
for i in range(271973, 785961 + 1):
    if valid(i):
        s += 1

print(s)
