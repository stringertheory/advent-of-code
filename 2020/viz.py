import json
import datetime

def isorted(iterator):
    return sorted(iterator, key=lambda x: int(x[0]))

with open('aoc-2015-2019-stats.json') as infile:
    data = json.load(infile)

for n_star in [1, 2]:
    for year, days in isorted(data.items()):
        for day, n_stars in isorted(days.items()):
            x = n_stars[str(n_star)]
            dt = datetime.date(int(year), 12, int(day))
            t10 = x[9]
            # print(day, x[99] / x[9], '"{}-{} ({:%a})"'.format(n_star, year, dt))
            value = x[99] / 60
            line = '{}\t{:.2f}\t"{}-{} ({:%a})"'.format(day, value, n_star, year, dt)
            print(line)
            # for i, n in enumerate(x):
            #     print(n, i + 1)
            # print()
        print()
    
    
