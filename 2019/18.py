"""
started at 8:23
first at 
second at
"""
import sys
import copy
import pprint
import itertools
import math
import collections
import datetime
import utils

import networkx as nx
from termcolor import colored


def make_graph(maze):
    graph = nx.Graph()
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val != "#":
                if (not y == 0) and maze[y - 1][x] != "#":
                    graph.add_edge((x, y), (x, y - 1))
                if (not y == (len(maze) - 1)) and maze[y + 1][x] != "#":
                    graph.add_edge((x, y), (x, y + 1))
                if (not x == 0) and maze[y][x - 1] != "#":
                    graph.add_edge((x, y), (x - 1, y))
                if (not x) == (len(row) - 1) and maze[y][x + 1] != "#":
                    graph.add_edge((x, y), (x + 1, y))

    starts = []
    doors = {}
    keys = {}
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val in {"@", "!", "$", "%", "&"}:
                starts.append((x, y))
            elif val.isupper():
                doors[val] = (x, y)
                graph.nodes[(x, y)]["door"] = val
            elif val.islower():
                keys[val] = (x, y)
                graph.nodes[(x, y)]["key"] = val

    return graph, starts, keys, doors


def draw_maze(maze, graph, positions):
    for y, row in enumerate(maze):
        this = []
        for x, c in enumerate(row):
            if c == "#":
                this.append(colored(c, "blue"))
            elif (x, y) in positions:
                this.append(colored("@", "yellow"))
            else:
                node = graph.nodes[(x, y)]
                if node.get("key"):
                    color = "green"
                    char = node.get("key")
                elif node.get("door"):
                    color = "red"
                    char = node.get("door")
                else:
                    color = "white"
                    char = "."
                this.append(colored(char, color))
        print("".join(this))


def immediate_keys(graph, position):
    to_visit = collections.deque()
    to_visit.append(position)
    distance = {position: 0}
    keys = {}
    doors = {}
    while to_visit:
        node = to_visit.popleft()
        d = distance[node]
        if graph.nodes[node].get("key"):
            keys[node] = d
        elif graph.nodes[node].get("door"):
            doors[node] = d
        else:
            for neighbor in graph.neighbors(node):
                if not neighbor in distance:
                    distance[neighbor] = d + 1
                    to_visit.append(neighbor)
    return keys


def memoize(function):
    from functools import wraps

    memo = {}

    @wraps(function)
    def wrapper(graph, start_nodes, start_keynames):

        remaining = tuple(
            n["key"] for i, n in sorted(graph.nodes.items()) if n.get("key")
        )
        key = (remaining, start_nodes, start_keynames)
        result = memo.get(key)
        if not result:
            result = function(graph, start_nodes, start_keynames)
            memo[key] = result
        return result

    return wrapper


@memoize
def all_paths(graph, start_nodes, start_keynames):

    print("=== all paths ===", start_keynames, start_nodes)

    neighbor_keys = {}
    for sn_index, start_node in enumerate(start_nodes):
        for key, n_steps in immediate_keys(graph, start_node).items():
            neighbor_keys[(sn_index, start_node, key)] = n_steps

    print("neighbors", start_keynames, neighbor_keys)

    result = []
    if not neighbor_keys:
        result.append((0, []))

    for (sn_index, key_from, key_to), n_steps in neighbor_keys.items():

        if n_steps == 0:
            print("n steps is 0", start_names, key_from, key_to)
            raise "WUT"

        clone = copy.deepcopy(graph)

        key_name = clone.nodes[key_to]["key"]
        clone.nodes[key_to]["key"] = None
        door = doors.get(key_name.upper())
        if door:
            clone.nodes[door]["door"] = None

        new_start_nodes = list(start_nodes)
        new_start_nodes[sn_index] = key_to
        new_keynames = list(start_keynames)
        new_keynames[sn_index] = key_name
        for path_length, path in all_paths(clone, tuple(new_start_nodes), tuple(new_keynames)):
            result.append((
                n_steps + path_length,
                [(sn_index, key_from, key_to, key_name)] + path,
            ))

    unique = set()
    shortest_unique = []
    for length, path in sorted(result):
        key = tuple(sorted(path))
        if not key in unique:
            shortest_unique.append((length, path))
            unique.add(key)

    print("$$$ unique", start_keynames, start_nodes, len(shortest_unique))
    print()
    sys.stdout.flush()
    return shortest_unique


def replace_center(maze):
    maze_array = []
    for y, row in enumerate(maze):
        maze_row = []
        for x, char in enumerate(row):
            maze_row.append(char)
            if char == "@":
                center = (x, y)
        maze_array.append(maze_row)

    x, y = center
    maze_array[y - 1][x - 1] = "!"
    maze_array[y - 1][x - 0] = "#"
    maze_array[y - 1][x + 1] = "$"
    maze_array[y - 0][x - 1] = "#"
    maze_array[y - 0][x - 0] = "#"
    maze_array[y - 0][x + 1] = "#"
    maze_array[y + 1][x - 1] = "%"
    maze_array[y + 1][x - 0] = "#"
    maze_array[y + 1][x + 1] = "&"

    result = ["".join(row) for row in maze_array]
    return result


maze = []
for line in utils.iterstrip("input-18.txt"):
    maze.append(line)

graph, starts, keys, doors = make_graph(maze)
draw_maze(maze, graph, starts)

part_one = all_paths(graph, tuple(starts), tuple("start" for i in starts))
shortest_part_one = list(sorted(part_one))[:5]

maze = replace_center(maze)

graph, starts, keys, doors = make_graph(maze)
draw_maze(maze, graph, starts)

part_two = all_paths(graph, tuple(starts), tuple("start" for i in starts))
shortest_part_two = list(sorted(part_two))[:5]

print("part one:")
for i, path in enumerate(shortest_part_one):
    length, array = path
    print(i + 1, length, "".join(i[3] for i in array))

print("part two:")
for i, path in enumerate(shortest_part_two):
    length, array = path
    print(i + 1, length, "".join(i[3] for i in array))
