import os.path
import shutil

def input_file(filename):
    if not os.path.isfile(filename):
        shutil.move('/Users/stringer/Downloads/input.txt', 'input.txt')

def iterstrip(filename='input.txt'):
    with open(filename) as infile:
        for line in infile:
            yield line.strip()

def iterdouble(filename='input.txt'):

    with open(filename) as infile:
        text = infile.read().strip()

    for chunk in text.split('\n\n'):
        yield chunk.strip()

            
def printmatrix(layer):
    from termcolor import colored
    colormap = {
        0: 'blue',
        1: 'white',
        2: 'green',
    }
    for y, row in enumerate(matrix):
        for x, value in enumerate(row):
            print(colored('█', colormap[value]), end='')
        print()
            

def print_squares(m, dead, start, end):
    xs = [x for x, y in m.keys()]
    ys = [y for x, y in m.keys()]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    board = []
    for y in range(y_min, y_max + 1):
        row = []
        for x in range(x_min, x_max + 1):
            char = m.get((x, y), ' ')
            if (x, y) == start:
                char = 'o'
            elif (x, y) == end:
                char = 'x'
            if (x, y) in dead:
                char = colored(char, 'red')
                
            row.append(char)
        board.append(row)

    for row in board:
        print(''.join(row))
    print()


def print_board(board, graph, current):
    for y, row in enumerate(board):
        this = []
        for x, c in enumerate(row):
            if c:
                if (x, y) == current:
                    this.append(colored('#', 'yellow'))
                elif graph.nodes[(x, y)].get('avoid'):
                    this.append(colored('#', 'red'))
                elif graph.nodes[(x, y)].get('marked'):
                    this.append(colored('#', 'green'))
                else:
                    this.append(colored('#', 'white'))
            else:
                this.append(' ')
        print(' '.join(this))


def draw_maze(maze, graph, start):
    for y, row in enumerate(maze):
        this = []
        for x, c in enumerate(row):
            if c == '#':
                this.append(colored(c, 'blue'))
            elif c == '@':
                this.append(colored(c, 'yellow'))
            elif c.islower():
                this.append(colored(c, 'green'))
            elif c.isupper():
                this.append(colored(c, 'red'))
            else:
                this.append(colored(c, 'white'))
        print(''.join(this))


def make_graph(maze):
    graph = nx.Graph()
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val != '#':
                if (not y == 0) and maze[y - 1][x] != '#':
                    graph.add_edge((x, y), (x, y - 1))
                if (not y == (len(maze) - 1)) and maze[y + 1][x] != '#':
                    graph.add_edge((x, y), (x, y + 1))
                if (not x == 0) and maze[y][x - 1] != '#':
                    graph.add_edge((x, y), (x - 1, y))
                if (not x) == (len(row) - 1) and maze[y][x + 1] != '#':
                    graph.add_edge((x, y), (x + 1, y))

    start = None
    doors = {}
    keys = {}
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val == '@':
                start = (x, y)
            elif val.isupper():
                doors[(x, y)] = val
            elif val.islower():
                keys[(x, y)] = val

    for xy, node in graph.nodes.items():

        door = doors.get(xy)
        if door:
            node['door'] = door
        else:
            node['door'] = None
            
        key = keys.get(xy)
        if key:
            node['key'] = key
        else:
            node['key'] = None
            
    return graph, start, keys, doors
        
def minmax(iterable):
    temp = tuple(iterable)
    return min(temp), max(temp)
        

