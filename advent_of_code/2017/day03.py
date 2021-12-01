# !/bin/python3
# http://www.adventofcode.com/2017/day/3

from math import sqrt, ceil
from utils import read_input


def get_closest_directional_values(radius):
    diameter = 2 * radius
    up = ((diameter - 1) * diameter) + radius + 1
    left = (diameter * diameter) + radius + 1
    right = ((diameter - 1) * (diameter - 1)) + radius
    down = ((diameter + 1) * diameter) + radius + 1
    return [up, left, right, down]


def get_dist_from_closest_directional(target, radius):
    values = get_closest_directional_values(radius)
    closest = target
    for value in values:
        abs_distance = abs(target - value)
        if abs_distance < closest:
            closest = abs_distance
    return closest


def get_radius(target):
    root = ceil(sqrt(target))
    if root % 2 == 0:
        root += 1
    return int(root / 2)


def get_dist_part_a(target):
    radius = get_radius(target)
    distance_from_closest_directional = get_dist_from_closest_directional(target, radius)
    return radius + distance_from_closest_directional


def get_next_direction(direction):
    if direction == 'right':
        return 'up'
    if direction == 'up':
        return 'left'
    if direction == 'left':
        return 'down'
    return 'right'


def insert_empty(matrix, direction):
    if direction == 'right':
        for row in matrix:
            row.append(None)
        return matrix
    if direction == 'up':
        matrix.insert(0, [None] * len(matrix[0]))
        return matrix
    if direction == 'left':
        for row in matrix:
            row.insert(0, None)
        return matrix
    matrix.append([None] * len(matrix[0]))
    return matrix


def get_next_coordinates(matrix, direction):
    if direction == 'right':
        i = len(matrix) - 1
        for j in range(1, len(matrix[i])):
            yield i, j
        return
    if direction == 'up':
        start_i = len(matrix) - 2
        if start_i < 0:
            start_i = 0
        j = len(matrix[0]) - 1
        if j < 0:
            j = 0
        for i in range(start_i, -1, -1):
            yield i, j
        return
    if direction == 'left':
        for j in range(len(matrix[0]) - 2, -1, -1):
            yield 0, j
        return
    for i in range(1, len(matrix)):
        yield i, 0


def get_adjacent_total(matrix, x, y):
    total = 0
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i < 0 or i > len(matrix) - 1:
                continue
            if j < 0 or j > len(matrix[i]) - 1:
                continue
            if not matrix[i][j]:
                continue
            total += matrix[i][j]
    return total


def get_dist_part_b(target):
    direction = 'down'
    val = 1
    matrix = [[1]]
    done = val > target

    while not done:
        direction = get_next_direction(direction)
        matrix = insert_empty(matrix, direction)
        for i, j in get_next_coordinates(matrix, direction):
            val = get_adjacent_total(matrix, i, j)
            matrix[i][j] = val
            if val > target:
                done = True
                break
    return val


TARGET = read_input(val_type=int)
print('part a:', get_dist_part_a(TARGET))
print('part b:', get_dist_part_b(TARGET))
