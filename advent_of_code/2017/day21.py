# !/bin/python3
# http://www.adventofcode.com/2017/day/21

from math import sqrt
from utils import read_input


def flip_x(grid):
    for i, row in enumerate(grid):
        grid[i] = row[::-1]
    return grid


def flip_y(grid):
    return grid[::-1]


def rotate(grid):
    rotated = [[] for x in grid]
    for row in grid:
        for i, col in enumerate(row):
            rotated[i].insert(0, col)
    return rotated


def get_string(grid):
    return '/'.join([''.join(row) for row in grid])


def find_match(grid, rules):
    joined = get_string(grid)
    if joined in rules.keys():
        return rules[joined]

    flipped = get_string(flip_x(grid))
    if flipped in rules.keys():
        return rules[flipped]
    flipped = get_string(flip_y(grid))
    if flipped in rules.keys():
        return rules[flipped]

    for _ in range(3):
        grid = rotate(grid)
        joined = get_string(grid)
        if joined in rules.keys():
            return rules[joined]


def get_split_grid(grid, skip):
    for i in range(0, len(grid), skip):
        for j in range(0, len(grid[i]), skip):
            current = []
            for k in range(skip):
                current.append(grid[i + k][j:j + skip])
            yield current


def get_joined_grid(grids):
    size = int(sqrt(len(grids)))
    grid_size = len(grids[0][0])
    joined = [[]]
    for i in range(0, size * grid_size, grid_size):
        for _ in range(size):
            for j, row in enumerate(grids.pop(0)):
                if i + j >= len(joined):
                    joined.append([])
                joined[i + j] += row
    return joined


def iterate(rules, num=1):
    grid = [['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]
    for _ in range(num):
        split_size = 2 if len(grid) % 2 == 0 else 3
        split = [find_match(x, rules) for x in get_split_grid(grid, split_size)]
        grid = get_joined_grid(split)
    return sum([x.count('#') for x in grid])
            

def parse_rules(rules):
    return {inp: [list(x) for x in out.split('/')] for inp, out in rules}


if __name__ == '__main__':
    RULES = parse_rules(read_input(separator=' => '))
    print('part a:', iterate(RULES, num=5))
    print('part b:', iterate(RULES, num=18))
