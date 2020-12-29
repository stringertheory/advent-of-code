import itertools
import utils


def find_invalid(parsed, n_preamble=25, n_combo=2, just_first=True):
    invalid = []
    for i in range(n_preamble, len(parsed)):
        n = parsed[i]
        preamble = parsed[(i - n_preamble):i]
        found = False
        for pair in itertools.combinations(preamble, n_combo):
            if sum(pair) == n:
                found = True
                break

        if not found:
            invalid.append(n)
            if just_first:
                break

    if just_first:
        return invalid[0]
    else:
        return invalid

parsed = [int(_) for _ in utils.iterstrip('input-09.txt')]
    
n = find_invalid(parsed, 25)
print(n)


for i in range(len(parsed)):
    s = 0
    contig = []
    for j in range(i, len(parsed)):
        contig.append(parsed[j])
        s += parsed[j]
        if s == n and len(contig) > 1:
            print(contig)
            print(min(contig) + max(contig))
            break
        elif s > n:
            break
        
               
                
