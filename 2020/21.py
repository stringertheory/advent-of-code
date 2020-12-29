import itertools
import collections
import utils

class Food:
    def __init__(self, id, ingredients, allergens):
        self.id = id
        self.ingredients = ingredients
        self.allergens = allergens

    def __repr__(self):
        return str(self.id)

allergens = set()
ingredients = set()

parsed = []
for index, line in enumerate(utils.iterstrip('input-21.txt')):
    allergen = line.split('(contains ')[-1].split(')')[0]
    a = set([_.strip() for _ in allergen.split(',')])
    i = set([_.strip() for _ in line.split('(')[0].split()])
    allergens.update(a)
    ingredients.update(i)
    parsed.append(Food(index, i, a))

print(allergens, len(ingredients))

nopes = collections.defaultdict(set)
for food in parsed:
    non_i = ingredients.difference(food.ingredients)
    a = food.allergens
    # print(food, non_i, a)
    for a in food.allergens:
        for i in non_i:
            nopes[i].add(a)

for a, b in itertools.combinations(parsed, 2):
    i_shared = a.ingredients.intersection(b.ingredients)
    i_union = a.ingredients.union(b.ingredients)
    i_diff = i_union.difference(i_shared)
    shared_a = a.allergens.intersection(b.allergens)
    # print(a, b, i_diff, shared_a)
    for ingredient in i_diff:
        for allergen in shared_a:
            nopes[ingredient].add(allergen)

result = {}
while len(result) < len(allergens):
    s = 0
    nons = set()
    for ingredient in ingredients:
        n = nopes.get(ingredient, set())
        if len(n) == len(allergens):
            nons.add(ingredient)
            s += 1
            # print(ingredient, len(n), n)

    yes = ingredients.difference(nons)

    part1 = 0
    for f in parsed:
        v = len(f.ingredients.intersection(nons))
        part1 += v

    # print(part1)
    # print(nopes)

    for ingredient in yes:
        poss = allergens.difference(nopes[ingredient])
        print(ingredient, nopes[ingredient], poss)
        if len(poss) == 1:
            found = poss.pop()
            result[ingredient] = found
            for ingredient in ingredients:
                if ingredient == found:
                    continue
                else:
                    nopes[ingredient].add(found)


print(','.join(i for (i, a) in sorted(result.items(), key=lambda i: i[1])))

