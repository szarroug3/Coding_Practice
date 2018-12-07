# !/bin/python3
# http://www.adventofcode.com/2017/day/22

from copy import deepcopy
from utils import read_input


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def infect(grid, bursts=1, advanced=False):
    direction = 0
    i = int(len(grid) / 2)
    j = int(len(grid[0]) / 2)
    num_infected = 0

    for _ in range(bursts):
        if advanced:
            # get next direction
            if grid[i][j] == '.':
                direction -= 1
                grid[i][j] = 'W'
            elif grid[i][j] == 'W':
                grid[i][j] = '#'
                num_infected += 1
            elif grid[i][j] == '#':
                direction += 1
                grid[i][j] = 'F'
            else:
                direction += 2
                grid[i][j] = '.'
        else:
            # infect or clean
            if grid[i][j] == '.':
                direction -= 1
                grid[i][j] = '#'
                num_infected += 1
            else:
                direction += 1
                grid[i][j] = '.'

        # move
        direction %= 4
        i += DIRECTIONS[direction][0]
        j += DIRECTIONS[direction][1]

        # create new grid space if needed
        while i < 0:
            grid.insert(0, ['.'] * len(grid[0]))
            i += 1
        while i >= len(grid):
            grid.append(['.'] * len(grid[0]))
        while j < 0:
            for row in grid:
                row.insert(0, '.')
            j += 1
        while j >= len(grid[0]):
            for row in grid:
                row.append('.')

    return num_infected


if __name__ == '__main__':
    GRID = [list(ROW) for ROW in read_input(separator=' => ')]
    print('part a:', infect(deepcopy(GRID), bursts=10000))
    print('part b:', infect(GRID, bursts=10000000, advanced=True))
