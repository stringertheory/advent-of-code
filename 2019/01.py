import math
import utils

def fuel(n, include_fuel=False):
    result = math.floor(n / 3) - 2
    if result <= 0:
        return 0
    else:
        if include_fuel:
            return result + fuel(result, include_fuel)
        else:
            return result
            
s = 0
f = 0
for line in utils.iterstrip('input-01.txt'):
    n = int(line)
    s += fuel(n)
    f += fuel(n, True)

print(s)
print(f)
