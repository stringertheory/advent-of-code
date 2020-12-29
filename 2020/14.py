import utils

mem = {}
key = None
value = None
for line in utils.iterstrip('input-14.txt'):
    if line.startswith('mask'):
        mask = line.split(' = ')[1].strip()
    elif line.startswith('mem'):
        key = int(line.split(']')[0].split('[')[1])
        value = int(line.split(' = ')[1].strip())
        binval = list("{0:036b}".format(value))
        for index, char in enumerate(mask):
            if char != 'X':
                binval[index] = char
        mem[key] = int(''.join(binval), 2)
            
print(sum(mem.values()))

def possible(string):
    nx = string.count('X')
    n = 2**nx
    for i in range(n):
        binval = "{:0{}b}".format(i, nx)
        result = []
        index = 0
        for j in string:
            if j == 'X':
                result.append(binval[index])
                index += 1
            else:
                result.append(j)
        # print(binval)
        # print(''.join(string))
        # print(''.join(result))
        assert result.count('X') == 0
        assert index == len(binval)
        yeah = ''.join(result)
        res = int(yeah, 2)
        yield yeah, res
    
mem = {}
key = None
value = None
for line in utils.iterstrip('input-14.txt'):
    if line.startswith('mask'):
        mask = line.split(' = ')[1].strip()
    elif line.startswith('mem'):
        key = int(line.split(']')[0].split('[')[1])
        binkey = list("{0:036b}".format(key))
        for index, char in enumerate(mask):
            if char == 'X':
                binkey[index] = 'X'
            elif char == '1':
                binkey[index] = '1'
        value = int(line.split(' = ')[1].strip())
        for i, (bink, new) in enumerate(possible(binkey)):
            mem[new] = value
        
print(sum(mem.values()))


