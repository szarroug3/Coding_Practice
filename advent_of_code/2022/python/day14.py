# !/bin/python3
# https://adventofcode.com/2022/day/14

from collections import defaultdict
from copy import deepcopy
from utils import read_input


def parse(line):
    values = []
    for coordinates in line.split(' -> '):
        values.append([int(x) for x in coordinates.split(',')])
    return values


def get_cave(rocks):
    cave = defaultdict(lambda: defaultdict(lambda: False))
    for rock in rocks:
        for i in range(1, len(rock)):
            cols = sorted([rock[i-1][0], rock[i][0]])
            rows = sorted([rock[i-1][1], rock[i][1]])

            for col in range(cols[0], cols[1]+1):
                for row in range(rows[0], rows[1]+1):
                    cave[row][col] = True

    return cave


def find_next(cave, prev, lowest):
    row, col = prev[-1]
    while True:
        if not cave[row+1][col]:
            row += 1
        elif not cave[row+1][col-1]:
            row += 1
            col -= 1
        elif not cave[row+1][col+1]:
            row += 1
            col += 1
        else:
            cave[row][col] = True
            return cave, prev

        prev.append((row, col))
        if row >= lowest:
            return cave, prev


def part_a(cave):
    lowest = max(cave.keys())
    total = 0

    last_row = 0
    prev = [(0, 500)]

    while last_row < lowest:
        cave, prev = find_next(cave, prev, lowest)
        last_row = prev.pop()[0]
        total += 1

    return total-1


def find_next_with_floor(cave, prev, floor):
    row, col = prev[-1]
    last_row, last_col = 0, 0

    while len(prev) > 0 and (row != last_row or col != last_col):
        last_row = row
        last_col = col
        append = True

        if row+1 == floor:
            prev.pop()
            break

        if not cave[row+1][col]:
            row += 1
        elif not cave[row+1][col-1]:
            row += 1
            col -= 1
        elif not cave[row+1][col+1]:
            row += 1
            col += 1
        else:
            row, col = prev.pop()
            append = False

        if append:
            prev.append((row, col))

    prev.append((row, col))
    cave[row][col] = True
    return cave, prev


def part_b(cave):
    floor = max(cave.keys()) + 2
    total = 0

    last = [(0, 0)]
    prev = [(0, 500)]

    while last != (0, 500):
        cave, prev = find_next_with_floor(cave, prev, floor)
        last = prev.pop()
        total += 1

    return total


if __name__ == '__main__':
    rocks = read_input(val_type=parse)
    cave = get_cave(rocks)

    print('part a:', part_a(deepcopy(cave)))
    print('part b:', part_b(deepcopy(cave)))
