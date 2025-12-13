# !/bin/python3

import math
from src.utils import read_input


def process_input(data):
    points = []
    for line in data:
        points.append([int(x) for x in line.split(',')])
    return points


def get_sorted_distances(points):
    # stored as a list of { distance, point_a, point_b }
    distances = []
    for i, (x1, y1, z1) in enumerate(points[:-1]):
        for j, (x2, y2, z2) in enumerate(points[i+1:]):
            distances.append({
                'distance': math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2),
                'point_a': [x1, y1, z1],
                'point_b': [x2, y2, z2]
            })

    return sorted(distances, key=lambda p: p['distance'])


def part_a(distances):
    circuits = []
    for curr in distances[:10]:
        a_index = None
        b_index = None
        for i, check in enumerate(circuits):
            if curr['point_a'] in check:
                a_index = i
            if curr['point_b'] in check:
                b_index = i
            if a_index and b_index:
                break

        # both are already connected, move on
        if a_index and a_index == b_index:
            continue

        # found both; merge the two indices
        if a_index and b_index:
            circuits[a_index].extend(circuits[b_index])
            del circuits[b_index]
        # only found point a, add point b to the circuit point a is on
        elif a_index:
            circuits[a_index].append(curr['point_b'])
        # only found point b, add point a to the circuit point b is on
        elif b_index:
            circuits[b_index].append(curr['point_a'])
        # found neither, create a new circuit
        else:
            circuits.append([curr['point_a'], curr['point_b']])

    lengths = sorted([len(circuit) for circuit in circuits], reverse=True)
    return lengths[0] * lengths[1] * lengths[2]


def part_b(points, distances):
    points_len = len(points)
    circuits = []
    for curr in distances:
        a_index = None
        b_index = None
        for i, check in enumerate(circuits):
            if curr['point_a'] in check:
                a_index = i
            if curr['point_b'] in check:
                b_index = i
            if a_index and b_index:
                break

        # both are already connected, move on
        if a_index is not None and a_index == b_index:
            continue

        # found both; merge the two indices
        if a_index is not None and b_index is not None:
            circuits[a_index].extend(circuits[b_index])
            del circuits[b_index]
        # only found point a, add point b to the circuit point a is on
        elif a_index is not None:
            circuits[a_index].append(curr['point_b'])
        # only found point b, add point a to the circuit point b is on
        elif b_index is not None:
            circuits[b_index].append(curr['point_a'])
        # found neither, create a new circuit
        else:
            circuits.append([curr['point_a'], curr['point_b']])

        if len(circuits) == 1 and len(circuits[0]) == points_len:
            return curr['point_a'][0] * curr['point_b'][0]


def main():
    points = process_input(read_input())
    sorted_distances = get_sorted_distances(points)
    print('part a:', part_a(sorted_distances))
    print('part b:', part_b(points, sorted_distances))


main()
