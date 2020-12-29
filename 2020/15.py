import collections

numbers = [0,14,1,3,7,9]
# numbers = [0,3,6]

said = []

encountered = collections.defaultdict(list)
for turn, n in enumerate(numbers, 1):
    encountered[n].append(turn)
    said.append(n)

off = 2020
off = 30000000
while len(said) < off:
    last = said[-1]
    if len(encountered[last]) < 2:
        said.append(0)
        encountered[0].append(len(said))
    else:
        diff = encountered[last][-1] - encountered[last][-2]
        # print(diff)
        said.append(diff)
        encountered[diff].append(len(said))
    # print(encountered)
    # print(said)
    # input()
    if not len(said) % (off / 100):
        print(len(said))

print(said[-1])

