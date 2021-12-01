# !/usr/bin/python3
# https://www.hackerrank.com/challenges/click-o-mania/problem


from collections import defaultdict


def get_connected(x, y, color, grid, visited=[], count=0):
    visited.append((x, y))
    if x - 1 >= 0 and grid[x - 1][y] == color and (x - 1, y) not in visited:
        count = get_connected(x - 1, y, color, grid, visited=visited, count=count)
    if y - 1 >= 0 and grid[x][y - 1] == color and (x, y - 1) not in visited:
        count = get_connected(x, y - 1, color, grid, visited=visited, count=count)
    if x + 1 < len(grid) and grid[x + 1][y] == color and (x + 1, y) not in visited:
        count = get_connected(x + 1, y, color, grid, visited=visited, count=count)
    if y + 1 < len(grid[x]) and grid[x][y + 1] == color and (x, y + 1) not in visited:
        count = get_connected(x, y + 1, color, grid, visited=visited, count=count)
    return count + 1


def get_groups(grid):
    groups = defaultdict(list)
    visited = []

    for i in range(len(grid)):
        for j, color in enumerate(grid[i]):
            if color == '-' or (i, j) in visited:
                continue
            visited.append((i, j))
            size = get_connected(i, j, color, grid, visited=visited)
            groups[color].append({'x': i, 'y': j, 'size': size})
    return groups


def get_largest_one_block_colors(groups):
    biggest_size = 1
    largest_group = None

    for group in groups.values():
        if len(group) != 1:
            continue
        if group[0]['size'] <= biggest_size:
            continue
        biggest_size = group[0]['size']
        largest_group = group[0]
    return largest_group


def get_largest_block_with_no_singles(groups):
    biggest_size = 0
    largest_group = None

    for group in groups.values():
        good = True
        biggest = 0
        largest = None

        for block in group:
            if block['size'] == 1:
                good = False
                break
            if block['size'] <= biggest:
                continue
            biggest = block['size']
            largest = block

        if not good:
            continue

        if biggest <= biggest_size:
            continue

        biggest_size = biggest
        largest_group = largest
    return largest_group


def get_largest_block(groups):
    biggest_size = 0
    largest_group = None

    for group in groups.values():
        for block in group:
            if block['size'] <= biggest_size:
                continue
            biggest_size = block['size']
            largest_group = block
    return largest_group

def next_move(grid):
    groups = get_groups(grid)

    largest_block = get_largest_one_block_colors(groups)
    if largest_block:
        print(largest_block['x'], largest_block['y'])
        return

    largest_block = get_largest_block_with_no_singles(groups)
    if largest_block:
        print(largest_block['x'], largest_block['y'])
        return

    largest_block = get_largest_block(groups)
    if largest_block:
        print(largest_block['x'], largest_block['y'])


if __name__ == '__main__':
    ROWS, COLUMNS, NUM_COLORS = [int(i) for i in input().strip().split()]
    GRID = []

    for _ in range(ROWS):
        GRID.append(list(input().strip()))

    next_move(GRID)
