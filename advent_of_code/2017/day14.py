# !/bin/python3
# http://www.adventofcode.com/2017/day/14

from utils import read_input
from day10 import get_knot_hash


def get_binary(knot_hash):
    binary = ''
    for c in knot_hash:
        integer = int(c, 16)
        binary += bin(integer)[2:].zfill(4)
    return binary


def get_row(hash):
    knot_hash = get_knot_hash(hash)
    binary = get_binary(knot_hash)
    return list(binary)


def get_square(hash):
    square = []
    for i in range(128):
        square.append(get_row('{0}-{1}'.format(hash, i)))
    return square


def get_num_used(square):
    count = 0
    for row in square:
        count += row.count('1')
    return count

def get_connected(x, y, square, visited=[]):
    visited.append((x, y))
    if x - 1 >= 0 and square[x - 1][y] == '1' and (x - 1, y) not in visited:
        yield x - 1, y
        yield from get_connected(x - 1, y, square, visited=visited)
    if y - 1 >= 0 and square[x][y - 1] == '1' and (x, y - 1) not in visited:
        yield x, y - 1
        yield from get_connected(x, y - 1, square, visited=visited)
    if x + 1 < 128 and square[x + 1][y] == '1' and (x + 1, y) not in visited:
        yield x + 1, y
        yield from get_connected(x + 1, y, square, visited=visited)
    if y + 1 < 128 and square[x][y + 1] == '1' and (x, y + 1) not in visited:
        yield x, y + 1
        yield from get_connected(x, y + 1, square, visited=visited)


def get_num_regions(square):
    region = 0
    regions = [[None] * 128 for _ in range(128)]

    for i in range(128):
        for j in range(128):
            # skip unused bits and bits that have already been assigned to a region
            if square[i][j] == '0' or regions[i][j]:
                continue

            # get adjacent used bits
            adjacent = [(k, l) for k, l in get_connected(i, j, square) if square[k][l] == '1']

            # if none of the adjacent regions have a region, assign one
            region += 1
            regions[i][j] = region
            for k, l in adjacent:
                regions[k][l] = region

    return region
            

if __name__ == '__main__':
    SQUARE = get_square(read_input())
    print('part a:', get_num_used(SQUARE))
    print('part b:', get_num_regions(SQUARE))
