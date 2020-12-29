"""Part two of this is a total hack...

"""
import itertools

import networkx as nx
from boltons import iterutils

s = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
"""

with open('input-19.txt') as infile:
    s = infile.read().strip()

def parse_rule(line):
    number, rules = line.split(': ')
    number = int(number)

    result = []
    if '|' in rules:
        first, second = rules.split(' | ')
        first = [int(i) for i in first.strip().split()]
        second = [int(i) for i in second.strip().split()]
        result = [first, second]
    else:
        try:
            first = [int(i) for i in rules.strip().split()]
        except ValueError:
            first = rules.strip().strip('"')
            result = [first]
        else:
            result = [first]

    return number, result

def make_graph(rules):

    graph = nx.DiGraph()
    for n, rule in rules.items():
        if len(rule) == 1:
            if rule[0] in ['a', 'b']:
                graph.nodes[n]['rules'] = rule
            else:
                for m in set(rule[0]):
                    graph.add_edge(n, m)
        elif len(rule) == 2:
            for k in rule:
                for m in set(k):
                    graph.add_edge(n, m)
        else:
            raise 'wut'

    return graph
    
def resolve_rules(rules, graph, ordered):
        
    for node in ordered:
        if graph.nodes[node].get('rules'):
            continue
        node_rules = []
        print(node, rules[node])
        for rule in rules[node]: # [[4, 4], [5, 5]]
            try:
                shee = [graph.nodes[_]['rules'] for _ in rule]
            except KeyError:
                print('shee', node, rule)
                continue
            for i in itertools.product(*shee):
                node_rules.append(''.join(i))
        graph.nodes[node]['rules'] = node_rules

    # result = {}
    # for node in graph.nodes:
    #     result[node] = graph.nodes[node]['rules']

    result = dict((n, d['rules']) for n, d in graph.nodes.items())

        
    return result

def match(string, n, rule):
    return string in rule


part1, part2 = s.strip().split('\n\n')

rules = {}
for line in part1.split('\n'):
    number, rule = parse_rule(line)
    rules[number] = rule

graph = make_graph(rules)
ordered = list(reversed(list(nx.topological_sort(graph))))

# rules[8] = [[42], [42, 8]]
# rules[11] = [[42, 31], [42, 11, 31]]
graph = make_graph(rules)

rules[0] = [[8, 11]]

rules = resolve_rules(rules, graph, ordered)
rule = set(rules[0])
print(len(rule))
print(list(sorted(rules[42])))
print(list(sorted(rules[31])))
def startmatch8(string, rule42):
    n = len(rule42[0])
    ruleset = set(rule42)
    n_match = 0
    possibles = []
    for chunk in iterutils.chunked(string, n):
        if chunk in ruleset:
            n_match += n
            possibles.append(n_match)
        else:
            break
    return possibles

def restmatch11(string, rule42, rule31):
    lrule = set(rule42)
    rrule = set(rule31)
    nl = len(rule42[0])
    nr = len(rule31[0])
    n = nl + nr
    if len(string) % n != 0:
        return False
    else:
        half = len(string) // 2
        firsthalf = string[:half]
        secondhalf = string[half:]
        for chunk in iterutils.chunked(firsthalf, nl):
            if chunk not in lrule:
                return False
        for chunk in iterutils.chunked(secondhalf, nr):
            if chunk not in rrule:
                return False

    return True

parsed = []
match0 = 0
for line in part2.split('\n'):
    ok = False
    for n_match in startmatch8(line, rules[42]):
        rest = line[n_match:]
        if rest and restmatch11(rest, rules[42], rules[31]):
            match0 += 1

print(match0)
    

