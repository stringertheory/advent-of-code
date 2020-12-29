"""For part one, I took an approach of finding the pieces that had
only two other matching cards -- those had to be the corners. That
worked pretty well, but... didn't require getting the exact matching
sequences right between rotated/flipped card sides.

In part two, I took an approach of placing one of the corners, then
placing subsequent piece to matching sides.

X...  XX..  XXX.  XXXX  XXXX  XXXX  etc...
....  ....  ....  ....  X...  XX..
....  ....  ....  ....  ....  ....

I ran into problems with placing pieces on the second and third row,
and it took a long time to debug. I was getting into situations where
there were no matches. Turns out I was not getting the matching
sequences incorrect. I would have spent a lot less time if I would
have been more careful to understand when a side matches with another
(in the __init__ of Tile). I think when I did part one, I realized
that I was being fast and loose with matching sequences, because I
knew I was only going for the count of matching cards and didn't have
to get which sides matched correctly. Maybe when I'd done that, it
would have been helpful to note (mentally, but also with a note in the
code) that if I need to do actual matching I should double check
whether I have the sequences and labels correct for the the code.

"""
import itertools
import math
import collections
import utils

SIDE_ORDER = ['T', 'R', 'B', 'L']

class Tile:

    def __init__(self, tile_id, chunks):
        self.id = tile_id
        self.chunks = chunks
        self.borders = {
            'T': self.chunks[0],
            'R': ''.join(row[-1] for row in self.chunks),
            'B': ''.join(reversed(self.chunks[-1])),
            'L': ''.join(reversed([row[0] for row in self.chunks])),
        }
        self.flipped_chunks = []
        for chunk in self.chunks:
            self.flipped_chunks.append(''.join(reversed(chunk)))
        self.flipped_borders = {
            'TF': ''.join(reversed(self.borders['T'])),
            'RF': ''.join(reversed(self.borders['L'])),
            'BF': ''.join(reversed(self.borders['B'])),
            'LF': ''.join(reversed(self.borders['R'])),
        }
        # print('\n'.join(self.chunks))
        # print()
        # print('\n'.join(self.flipped_chunks))
        # print()
        # print(self.borders)
        # print()
        # print(self.flipped_borders)
    
    def __repr__(self):
        return '\n'.join(self.chunks)
    
    def print(self, orientation):
        if orientation == 'top':
            return '\n'.join(self.chunks)
        
    def get_chunk(self, index, orientation):
        rotated = self.chunks
        if orientation.endswith('F'):
            n_rotate = SIDE_ORDER.index(orientation[0])
            rotated = [''.join(reversed(c)) for c in self.chunks]
        else:
            n_rotate = SIDE_ORDER.index(orientation)

        for i in range(n_rotate):
            rotated = [''.join(_) for _ in list(zip(*rotated))[::-1]]

        return rotated[index]
    
    def all_borders(self, include_flip=False):
        for i in self.borders.items():
            yield i
        if include_flip:
            for i in self.flipped_borders.items():
                yield i

    def matches(self, other):
        result = []
        for a, border_a in self.all_borders(include_flip=True):
            for b, border_b in other.all_borders(include_flip=True):
                if tuple(border_a) == tuple(reversed(border_b)):
                    result.append((a, b))
        return result

class Board(list):
    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny
        for y in range(ny):
            row = []
            for x in range(nx):
                row.append((None, None))
            self.append(row)

    def print(self, tiles):
        for row in self:
            self.print_row(row, tiles)
            print()
            
    def print_row(self, row, tiles):
        first_tile_id = self[0][0][0]
        first_tile = tiles[first_tile_id]
        chunk_width = len(first_tile.chunks[0])
        n_chunks = len(first_tile.chunks)

        chunk_row = []
        for tile_id, orientation in row:
            label = ''
            if tile_id is not None:
                label = '{} ({})'.format(tile_id, orientation)
            chunk_row.append(label.center(chunk_width))
        print(' '.join(chunk_row))
        
        for chunk_index in range(n_chunks):
            chunk_row = []
            for tile_id, orientation in row:
                tile = tiles.get(tile_id)
                if tile:
                    chunk = tile.get_chunk(chunk_index, orientation)
                else:
                    chunk = '?' * chunk_width
                chunk_row.append(chunk)
            print(' '.join(chunk_row))

    def print_inner(self, tiles, filename):
        with open(filename, 'w') as outfile:
            for row in self:
                self.print_row_inner(row, tiles, outfile)
            
    def print_row_inner(self, row, tiles, outfile):
        first_tile_id = self[0][0][0]
        first_tile = tiles[first_tile_id]
        chunk_width = len(first_tile.chunks[0])
        n_chunks = len(first_tile.chunks)
        
        for chunk_index in range(1, n_chunks - 1):
            chunk_row = []
            for tile_id, orientation in row:
                tile = tiles.get(tile_id)
                if tile:
                    chunk = tile.get_chunk(chunk_index, orientation)[1:-1]
                else:
                    chunk = '?' * (chunk_width - 2)
                chunk_row.append(chunk)
            print(''.join(chunk_row), file=outfile)
            
a = Tile(1, """123
456
789
""".splitlines())

a.get_chunk(0, 'T')


b = Tile(2, """123
000
000
""".splitlines())


parsed = {}
for chunk in utils.iterdouble('input-20.txt'):
    chunks = chunk.splitlines()
    tile = int(chunks[0].split()[-1].strip(':'))
    parsed[tile] = Tile(tile, chunks[1:])

# parsed = {
#     1: a,
#     2: b,
# }

match_lookup = {}
matches = collections.defaultdict(dict)
for tile_a, tile_b in itertools.combinations(parsed.values(), 2):

    ab = tile_a.matches(tile_b)
    if ab:
        matches[tile_a.id][tile_b.id] = ab
        for a_side, b_side in ab:
            match_lookup[(tile_a.id, a_side)] = (tile_b.id, b_side)

    ba = tile_b.matches(tile_a)
    if ba:
        matches[tile_b.id][tile_a.id] = ba
        for b_side, a_side in ba:
            match_lookup[(tile_b.id, b_side)] = (tile_a.id, a_side)

# for a, b in sorted(match_lookup.items()):
#     print(a, b)
# raise "STOP"
            
corners = []
pieces = []
for tile_id in sorted(parsed):
    # print(tile_id, len(matches[tile_id]))
    n_match = len(matches[tile_id])
    pieces.append((n_match, tile_id, parsed[tile_id]))
    if n_match == 2:
        corners.append(tile_id)


        
pieces.sort(reverse=True)

n = int(math.sqrt(len(parsed)))
board = Board(n, n)

n_matches, piece_id, piece = pieces.pop()
# print(piece_id, matches[piece_id])
board[0][0] = (piece_id, 'T')




for i in range(1, len(board)**2):
    x, y = (i % len(board), i // len(board))
    left_id, left_orientation = None, None
    top_id, top_orientation = None, None
    if x > 0:
        left_i = i - 1
        left_x, left_y = (left_i % len(board), left_i // len(board))
        left_id, left_orientation = board[left_y][left_x]
    if y > 0:
        top_i = i - len(board)
        top_x, top_y = (top_i % len(board), top_i // len(board))
        top_id, top_orientation = board[top_y][top_x]

    print(i, y, x, (left_id, left_orientation), (top_id, top_orientation))

    left_r_side = None
    if left_orientation is not None:
        left_rs_index = SIDE_ORDER.index(left_orientation[0]) + 1
        left_r_side = SIDE_ORDER[left_rs_index % len(SIDE_ORDER)]
        if left_orientation.endswith('F'):
            left_r_side += 'F'

    top_b_side = None
    if top_orientation is not None:
        top_bs_index = SIDE_ORDER.index(top_orientation[0]) + 2
        top_b_side = SIDE_ORDER[top_bs_index % len(SIDE_ORDER)]
        if top_orientation.endswith('F'):
            top_b_side += 'F'
        
    print(i, y, x, left_r_side, top_b_side)
    print(matches[left_id])
    # print(match_lookup[(left_id, left_r_side)])
    this_piece_id, this_left_side = None, None
    if left_id:
        try:
            this_piece_id, this_left_side = match_lookup[(left_id, left_r_side)]
        except KeyError:
            print()
            board.print(parsed)
            raise

    if this_left_side is not None:
        top_this_index = SIDE_ORDER.index(this_left_side[0]) + 1
        this_orientation = SIDE_ORDER[top_this_index % len(SIDE_ORDER)]
        if this_left_side.endswith('F'):
            this_orientation += 'F'

    if this_piece_id is None:

        print(matches[top_id])
        for a, b in match_lookup.items():
            if a[0] == top_id:
                print('hi', [a, b])
        print('not', [top_id, top_b_side, top_orientation])

        this_piece_id, this_top_side = None, None
        if top_id:
            this_piece_id, this_top_side = match_lookup[(top_id, top_b_side)]
        
        if this_top_side is not None:
            top_this_index = SIDE_ORDER.index(this_top_side[0])
            this_orientation = SIDE_ORDER[top_this_index % len(SIDE_ORDER)]
            if this_top_side.endswith('F'):
                this_orientation += 'F'

    if not this_piece_id:
        board.print(parsed)
        raise 'damn'
                
    print(i, y, x, this_piece_id, this_orientation)
    board[y][x] = (this_piece_id, this_orientation)
    # if x == 0:
    #     print(this_piece_id)
    #     print(parsed[this_piece_id])
    #     print()
        
    # raise 'STOP'

board.print(parsed)
filename = 'output-20.txt'
board.print_inner(parsed, filename)

def find_dragons(puzzle, mask):
    result = []
    puzzle_width = len(puzzle[0])
    puzzle_height = len(puzzle)
    mask_width = max(x for x, y in mask) + 0
    mask_height = max(y for x, y in mask) + 0
    for y in range(puzzle_height - mask_height):
        for x in range(puzzle_width - mask_width):
            found = all(puzzle[y + dy][x + dx] == '#' for dx, dy in mask)
            if found:
                result.append((x, y, tuple((x + dx, y + dy) for dx, dy in mask)))

    return result
dragon = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".lstrip('\n')
print(dragon)

mask = set()
for y_offset, row in enumerate(dragon.splitlines()):
    for x_offset, char in enumerate(row):
        if char == '#':
            mask.add((x_offset, y_offset))

puzzle = []
with open(filename) as infile:
    for line in infile:
        puzzle.append(line.strip())

a = find_dragons(puzzle, mask)
if not a:
    for i in range(3):
        puzzle = [''.join(_) for _ in list(zip(*puzzle))[::-1]]
        a = find_dragons(puzzle, mask)
        if a:
            break

flipped_puzzle = []
for chunk in puzzle:
    flipped_puzzle.append(''.join(reversed(chunk)))

puzzle = flipped_puzzle
    
a = find_dragons(puzzle, mask)
if not a:
    for i in range(3):
        puzzle = [''.join(_) for _ in list(zip(*puzzle))[::-1]]
        a = find_dragons(puzzle, mask)
        if a:
            break

def replace_dragons(puzzle, offsets):
    array_puzzle = [list(row) for row in puzzle]
    for x0, y0, replace_list in offsets:
        for (x, y) in replace_list:
            array_puzzle[y][x] = '0'
    return '\n'.join([''.join(row) for row in array_puzzle])
        
new = replace_dragons(puzzle, a)
print(new)
print(math.prod(corners))
print(new.count('#'))

    
# for row in board:
#     for piece_id, orientation in row:
#         print(piece_id, orientation)
#         piece = parsed[piece_id]
#         print(piece)
#         print()
    
# # print(pieces)

# print(len(parsed))
# print(corners)
# print(math.prod(corners))
    

