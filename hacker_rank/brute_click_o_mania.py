# !/usr/bin/python3
# https://www.hackerrank.com/challenges/click-o-mania/problem


from copy import deepcopy
from collections import defaultdict


def get_connected(x, y, color, grid, visited):
    visited.append((x, y))
    if x - 1 >= 0 and grid[x - 1][y] == color and (x - 1, y) not in visited:
        visited = get_connected(x - 1, y, color, grid, visited)
    if y - 1 >= 0 and grid[x][y - 1] == color and (x, y - 1) not in visited:
        visited = get_connected(x, y - 1, color, grid, visited)
    if x + 1 < len(grid) and grid[x + 1][y] == color and (x + 1, y) not in visited:
        visited = get_connected(x + 1, y, color, grid, visited)
    if y + 1 < len(grid[x]) and grid[x][y + 1] == color and (x, y + 1) not in visited:
        visited = get_connected(x, y + 1, color, grid, visited)
    return visited


def get_groups(grid):
    groups = []
    visited = []

    for i, row in enumerate(grid):
        if row.count('-') == len(row):
            continue
        for j, color in enumerate(row):
            if color == '-' or (i, j) in visited:
                continue

            connected = get_connected(i, j, color, grid, [])

            # ignore groups of size 1 since we can't remove them
            if len(connected) == 1:
                continue

            visited += connected
            groups.append(connected)
    groups.sort(key=len)
    return groups[::-1]


def grid_has_blocks(grid):
    for row in grid:
        if row.count('-') < len(row):
            return True
    return False


def look_for_next_block_up(grid, x, y):
    for i in range(x - 1, -1, -1):
        if grid[i][y] == '-':
            continue
        return i


def remove_and_settle(grid, group):
    # remove blocks in group
    for i, j in group:
        grid[i][j] = '-'

    # settle by moving blocks down
    for i in range(len(grid) - 1, -1, -1):
        for j in range(len(grid[i])):
            if grid[i][j] != '-':
                continue
            k = look_for_next_block_up(grid, i, j)
            if k is None:
                continue
            grid[i][j] = grid[k][j]
            grid[k][j] = '-'

    # settle by moving blocks left
    last_row = len(grid) - 1
    j = -1
    while j < len(grid[last_row]) - 1:
        j += 1
        # stop if there are no more columns with stuff towards the right
        if grid[last_row][j:].count('-') == len(grid[last_row][j:]):
            break
        # skip columns with stuff in them
        if grid[last_row][j] != '-':
            continue
        for row in grid:
            row.pop(j)
            row.append('-')
        j -= 1

    return grid


def try_moves(grid):
    print_grid(grid)
    groups = get_groups(grid)
    for group in groups:
        temp_grid = remove_and_settle(deepcopy(grid), group)
        if not grid_has_blocks(temp_grid):
            return group

        if try_moves(temp_grid):
            return group

# TODO: remove
def print_grid(grid):
    print('      ', ' '.join([str(x) for x in range(len(grid[0]))]))
    for i, row in enumerate(grid):
        print(str(i).zfill(2), '   ', ' '.join(row))


def next_move(grid):
    group = try_moves(grid)
    if group:
        print(group[0][0], group[0][1])


if __name__ == '__main__':
    ROWS, COLUMNS, NUM_COLORS = [int(i) for i in input().strip().split()]
    GRID = []

    for _ in range(ROWS):
        GRID.append(list(input().strip()))

    next_move(GRID)
