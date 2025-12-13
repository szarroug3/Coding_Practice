# !/bin/python3

from copy import deepcopy
from src.utils import read_input


def process_input(data):
    grid = []
    for line in data:
        grid.append(list(line))
    return grid


def get_directions():
    directions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i or j:
                directions.append([i, j])
    return directions


def get_accessible(grid):
    accessible = []
    col_len = len(grid)
    row_len = len(grid[0])
    directions = get_directions()

    for i, line in enumerate(grid):
        for j, value in enumerate(line):
            if value != '@':
                continue

            curr = 0
            for x, y in directions:
                new_i = i + x
                new_j = j + y
                if new_i >= 0 and new_i < col_len and new_j >= 0 and new_j < row_len and grid[new_i][new_j] == '@':
                    curr += 1
                    if curr >= 4:
                        break
            if curr < 4:
                accessible.append([i, j])
    return accessible


def part_a(grid):
    return len((get_accessible(grid)))


def part_b(grid):
    count = 0
    accessible = get_accessible(grid)
    while accessible:
        count += len(accessible)
        for i, j in accessible:
            grid[i][j] = '.'
        accessible = get_accessible(grid)
    return count


def main():
    instructions = process_input(read_input())
    print('part a:', part_a(instructions))
    print('part b:', part_b(instructions))


main()
