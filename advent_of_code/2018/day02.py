# !/bin/python3
# https://adventofcode.com/2018/day/2

from utils import read_input
from collections import defaultdict


def get_two_three(box_id):
    two = 0
    three = 0
    for id in set(box_id):
        count = box_id.count(id)
        if count == 2:
            two = 1
        elif count == 3:
            three = 1

        if two and three:
            break
    return two, three


def get_hash(box_ids):
    two_count = 0
    three_count = 0
    for box_id in box_ids:
        two, three = get_two_three(box_id)
        two_count += two
        three_count += three
    return two_count * three_count


def find_common_letters(a, b):
    diff = False
    same = ''
    for i, letter in enumerate(a):
        if letter == b[i]:
            same += letter
        else:
            if diff:
                return None
            diff = True
    return same


def find_common_box_ids(box_ids):
    for i, first in enumerate(box_ids):
        for second in box_ids[i+1:]:
            common = find_common_letters(first, second)
            if common:
                return common


if __name__ == '__main__':
    box_ids = read_input()
    print('part a:', get_hash(box_ids))
    print('part b:', find_common_box_ids(box_ids))
