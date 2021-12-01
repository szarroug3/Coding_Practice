# !/bin/python3
# https://adventofcode.com/2018/day/13


from copy import deepcopy
from collections import defaultdict, deque
from utils import read_input


directions = {'^': 'up', '<': 'left', 'v': 'down', '>': 'right'}
move = {'left': (0, -1), 'right': (0, 1),
        'up': (-1, 0), 'down': (1, 0)}
intersection = {'up': {'left': 'left', 'right': 'right'},
                'down':  {'left': 'right', 'right': 'left'},
                'left': {'left': 'down', 'right': 'up'},
                'right': {'left': 'up', 'right': 'down'}}
tracks = {'/': {'track': '/', 'up': 'right', 'down': 'left', 'left': 'down', 'right': 'up'},
          '\\': {'track': '\\', 'up': 'left', 'down': 'right', 'left': 'up', 'right': 'down'},
          '-': {'track': '-'},
          '|': {'track': '|'},
          '+': {'track': '+'}}


def parse(lines):
    grid = defaultdict(lambda: defaultdict(dict))
    elves = []
    for y, line in enumerate(lines):
        for x, track in enumerate(line):
            if not track:
                continue
            if track in directions.keys():
                elves.append({'x': x, 'y': y, 'active': True,
                              'curr': directions[track],
                              'next': deque(['left', 'straight', 'right'])})
                grid[y][x] = deepcopy(tracks['-' if track in ['<', '>'] else '|'])
                grid[y][x]['occupied'] = elves[-1]
                continue
            if track in tracks.keys():
                grid[y][x] = deepcopy(tracks[track])
                grid[y][x]['occupied'] = None
    return grid, elves


def go(grid, elves):
    remove = []
    first = None
    while True:
        elves = sorted([e for e in elves if e['active']], key=lambda loc: (loc['y'], loc['x']))
        if len(elves) == 1:
            return first[0], first[1], elves[0]['x'], elves[0]['y']
        for elf in elves:
            if not elf['active']:
                continue

            x = elf['x']
            y = elf['y']
            curr = elf['curr']
            y_move, x_move = move[curr]

            grid[y][x]['occupied'] = None
            x += x_move
            y += y_move
            elf['x'] = x
            elf['y'] = y

            if grid[y][x]['occupied'] and grid[y][x]['occupied']['active']:
                if not first:
                    first = (x, y)

                elf['active'] = False
                grid[y][x]['occupied']['active'] = False
                grid[y][x]['occupied'] = None

            grid[y][x]['occupied'] = elf

            if grid[y][x]['track'] == '+':
                next_dir = elf['next'][0]
                elf['next'].rotate(-1)
                if next_dir != 'straight':
                    elf['curr'] = intersection[curr][next_dir]
            elif curr in grid[y][x]:
                elf['curr'] = grid[y][x][curr]

        remove = []


if __name__ == '__main__':
    import pprint
    grid, elves = parse(read_input(ignore_empty=False, val_type=list))
    # pprint.pprint(elves)
    first_x, first_y, last_x, last_y = go(grid, elves)
    print('part a:', (first_x, first_y))
    print('part b:', (last_x, last_y))
