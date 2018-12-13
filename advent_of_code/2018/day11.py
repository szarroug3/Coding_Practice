# !/bin/python3
# https://adventofcode.com/2018/day/11

import numpy

from utils import read_input

serial = 0

def get_power(x, y):
    x += 1
    y += 1
    rack = x + 10
    power = ((rack * y) + serial) * rack
    return (power // 100 % 10) - 5


def get_biggest(grid, size):
    for width in range(3, 300):
        block = sum(grid[x:x-width+1 or None, y:y-width+1 or None] for x in range(width) for y in range(width))
        maximum = int(block.max())
        loc = numpy.where(block == maximum)
    return loc[0][0] + 1, loc[1][0] + 1, maximum


def get_biggest_size(grid):
    maximum = grid[0][0]
    data = (1, 1, 1)
    for i in range(1, 301):
        x, y, m = get_biggest(grid, i)
        if m > maximum:
            maximum = m
            data = (x, y, size)
    return data


if __name__ == '__main__':
    serial += read_input(val_type=int)
    grid = numpy.fromfunction(get_power, (300, 300))
    print('part a:', get_biggest(grid, 3)[:2])
    print('part b:', get_biggest_size(grid))
