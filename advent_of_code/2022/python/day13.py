# !/bin/python3
# https://adventofcode.com/2022/day/13

import json

from collections import defaultdict
from copy import copy
from itertools import combinations
from utils import read_input


def compare_ints(left, right):
    if left < right:
        return True
    if left > right:
        return False


def compare_lists(left, right):
    for index in range(max(len(left), len(right))):
        if index >= len(left):
            # left ran out first
            if index < len(right):
                return True
            # they both ran out, continue
            if index >= len(right):
                return

        # right ran out first
        if index >= len(right):
            return False

        # at this point, we know both sides have a value at the current index
        result = compare(left[index], right[index])
        if result is not None:
            return result


def compare_mixed(left, right):
    if type(left) is not list:
        left = [left]
    if type(right) is not list:
        right = [right]
    return left, right


def compare(left, right):
    if type(left) is int and type(right) is int:
        func = compare_ints
    elif type(left) is list and type(right) is list:
        func = compare_lists
    else:
        left, right = compare_mixed(left, right)
        return compare(left, right)

    return func(left, right)


def part_a(pairs):
    total = 0
    for i, (left, right) in enumerate(pairs, 1):
        if compare(left, right):
            total += i
    return total


def find_correct(packets):
    correct = {i: [] for i in range(len(packets))}

    for left, right in combinations(range(len(packets)), 2):
        if compare(packets[left], packets[right]):
            correct[left].append(right)

        if compare(packets[right], packets[left]):
            correct[right].append(left)

    return correct


def find_next(correct):
    for key, value in correct.items():
        if len(value) == 0:
            return key


def remove_packet(correct, packet):
    del correct[packet]
    for key in correct.keys():
        correct[key].remove(packet)
    return correct


def find_order(correct):
    order = []
    while correct:
        packet = find_next(correct)
        order.insert(0, packet)
        remove_packet(correct, packet)
    return order


def part_b(pairs):
    packets = [[[2]], [[6]]]
    for pair in pairs:
        packets.extend(pair)

    correct = find_correct(packets)
    order = find_order(correct)
    return (order.index(0) + 1) * (order.index(1) + 1)


if __name__ == '__main__':
    pairs = read_input(delimiter='\n\n', line_delimiter='\n',
                       val_type=json.loads)

    print('part a:', part_a(pairs))
    print('part b:', part_b(pairs))
