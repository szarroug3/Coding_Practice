# !/bin/python3
# https://adventofcode.com/2022/day/4

from utils import read_input


def parse(sections):
    data = []
    for pair in sections:
        curr = []
        for elf in pair:
            curr.append([int(x) for x in elf.split("-")])
        data.append(curr)

    return data


def check_complete_inclusion(a, b):
    if a[0] >= b[0] and a[1] <= b[1]:
        return True
    if b[0] >= a[0] and b[1] <= a[1]:
        return True
    return False


def part_a(sections):
    total = 0
    for section in sections:
        if check_complete_inclusion(*section):
            total += 1
    return total


def check_partial_inclusion(a, b):
    if b[1] >= a[0] >= b[0]:
        return True
    if b[1] >= a[1] >= b[0]:
        return True
    if a[1] >= b[0] >= a[0]:
        return True
    if a[1] >= b[1] >= a[0]:
        return True
    return False


def part_b(sections):
    total = 0
    for section in sections:
        if check_partial_inclusion(*section):
            total += 1
    return total


if __name__ == "__main__":
    sections = parse(
        read_input(
            line_delimiter=",",
        )
    )

    print("part a:", part_a(sections))
    print("part b:", part_b(sections))
