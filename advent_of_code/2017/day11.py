# !/bin/python3
# http://www.adventofcode.com/2017/day/11

from utils import read_input


def calculate_distance(north, northeast, northwest):
    done = False
    while not done:
        done = True
        if northeast > 0 and northwest > 0:
            val = northeast if northeast < northwest else northwest
            north += val
            northeast -= val
            northwest -= val
            done = False
        if northeast < 0 and northwest < 0:
            val = abs(northeast) if northeast > northwest else abs(northwest)
            north -= val
            northeast += val
            northwest += val
            done = False
        if northeast > 0 and north < 0:
            val = northeast if northeast > abs(north) else abs(north)
            northeast -= val
            north += val
            northwest -= val
            done = False
        if northeast < 0 and north > 0:
            val = abs(northeast) if abs(northeast) < north else north
            northeast += val
            north -= val
            northwest += val
            done = False
        if northwest > 0 and north < 0:
            val = northwest if northwest > abs(north) else abs(north)
            northwest -= val
            north += val
            northeast -= val
            done = False
        if northwest < 0 and north > 0:
            val = abs(northwest) if abs(northwest) < north else north
            northwest += val
            north -= val
            northeast += val
            done = False
    return abs(north) + abs(northeast) + abs(northwest)


def get_distance(directions):
    north = 0
    northeast = 0
    northwest = 0
    max_distance = 0
    current_distance = 0

    for direction in directions:
        if direction == 'n':
            north += 1
        elif direction == 's':
            north -= 1
        elif direction == 'ne':
            northeast += 1
        elif direction == 'sw':
            northeast -= 1
        elif direction == 'nw':
            northwest += 1
        elif direction == 'se':
            northwest -= 1
        current_distance = calculate_distance(north, northeast, northwest)
        if current_distance > max_distance:
            max_distance = current_distance
    return current_distance, max_distance


DIRECTIONS = read_input(separator=',')
CURRENT_DISTANCE, MAX_DISTANCE = get_distance(DIRECTIONS)
print('part a:', CURRENT_DISTANCE)
print('part b:', MAX_DISTANCE)
