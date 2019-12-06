# !/bin/python3
# https://adventofcode.com/2019/day/3

from utils import read_input


def get_wire_coordinates(wire):
    direction = {'U': up, 'D': down, 'L': left, 'R': right}
    coordinates = [(0, 0)]
    x, y = 0, 0
    for data in wire.split(','):
        func = direction[data[0]]
        distance = int(data[1:])
        coordinates.extend(func(x, y, distance))
        x, y = coordinates[-1]
    return coordinates


def up(x, y, distance):
    coordinates = []
    for i in range(1, distance+1):
        coordinates.append((x, y - i))
    return coordinates


def down(x, y, distance):
    coordinates = []
    for i in range(1, distance+1):
        coordinates.append((x, y + i))
    return coordinates


def left(x, y, distance):
    coordinates = []
    for i in range(1, distance+1):
        coordinates.append((x - i, y))
    return coordinates


def right(x, y, distance):
    coordinates = []
    for i in range(1, distance+1):
        coordinates.append((x + i, y))
    return coordinates


def get_shortest_distance(wire_a, wire_b):
    shortest = None
    for wire_x, wire_y in set(wire_a[1:]).intersection(set(wire_b[1:])):
        distance = abs(wire_x) + abs(wire_y)
        if shortest is None or distance < shortest:
            shortest = distance

    return shortest


def get_shortest_travel(wire_a, wire_b):
    shortest = None
    for wire_x, wire_y in set(wire_a[1:]).intersection(set(wire_b[1:])):
        length_a = wire_a.index((wire_x, wire_y))
        length_b = wire_b.index((wire_x, wire_y))
        distance = abs(length_a) + abs(length_b)
        if shortest is None or distance < shortest:
            shortest = distance

    return shortest


if __name__ == '__main__':
    wire_a, wire_b = [get_wire_coordinates(data) for data in read_input(val_type=str)]
    print('part a:', get_shortest_distance(wire_a, wire_b))
    print('part b:', get_shortest_travel(wire_a, wire_b))
