# !/bin/python3

from copy import deepcopy
from collections import defaultdict
from src.utils import read_input


TURN = {
    '^': '>',
    '>': 'V',
    'V': '<',
    '<': '^'
}

WALK = {
    '^': [-1, 0],
    '>': [0, 1],
    'V': [1, 0],
    '<': [0, -1]
}

def process_input(data):
    lab = [list(line) for line in data]
    start_y = None
    start_x = None
    direction = None
    
    for i, line in enumerate(lab):
        start_y = i
        if '^' in line:
            start_x = line.index('^')
            direction = '^'
        if '>' in line:
            start_x = line.index('>')
            direction = '>'
        if 'V' in line:
            start_x = line.index('V')
            direction = 'V'
        if '<' in line:
            start_x = line.index('<')
            direction = '<'

        if direction:
            break

    return lab, start_y, start_x, direction

def find_path(lab, y, x, direction):
    visited = defaultdict(lambda: defaultdict(list))
    
    while y != -1 and y != len(lab) and x != -1 and x != len(lab[y]) and direction not in visited[y][x]:
        visited[y][x].append(direction)
        y, x, direction = traverse(lab, y, x, direction)

    out_of_range = y == -1 or y == len(lab) or x == -1 or x == len(lab[y])
    return visited, not out_of_range
    
def traverse(lab, y, x, direction):
    walk = WALK[direction]
    new_y = y + walk[0]
    new_x = x + walk[1]
    
    while new_y == -1 or new_y == len(lab) or new_x == -1 or new_x == len(lab[new_y]) or lab[new_y][new_x] == '#':
        if new_y == -1 or new_y == len(lab) or new_x == -1 or new_x == len(lab[new_y]):
            return new_y, new_x, direction

        direction = TURN[direction]
        walk = WALK[direction]
        new_y = y + walk[0]
        new_x = x + walk[1]
        
    return new_y, new_x, direction
    

def part_a(lab, y, x, direction):
    visited, _ = find_path(lab, y, x, direction)
    return sum(len(vals) for vals in visited.values())


def part_b(lab, start_y, start_x, direction):
    count = 0
    path, _ = find_path(lab, start_y, start_x, direction)
    for y in path:
        for x in path[y]:
            if start_y == y and start_x == x:
                continue

            lab_copy = deepcopy(lab)
            lab_copy[y][x] = '#'
            _, infinite = find_path(lab_copy, start_y, start_x, direction)

            if infinite:
                count += 1
            
    return count


def main():
    data = read_input()
    lab, start_y, start_x, direction = process_input(data)
    print(part_a(lab, start_y, start_x, direction))
    print(part_b(lab, start_y, start_x, direction))


main()
