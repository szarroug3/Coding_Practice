# !/bin/python3
# https://adventofcode.com/2022/day/3

from utils import read_input


def get_priority(value):
    priority = ord(value)

    if priority >= 65 and priority <= 90:
        return priority - 38
    return priority - 96


def part_a(rucksacks):
    total = 0

    for rucksack in rucksacks:
        length = int(len(rucksack) / 2)
        a = set(rucksack[:length])
        b = set(rucksack[length:])
        duplicate = a.intersection(b).pop()
        total += get_priority(duplicate)

    return total


def part_b(rucksacks):
    total = 0

    for i in range(0, len(rucksacks), 3):
        a = set(rucksacks[i])
        b = set(rucksacks[i + 1])
        c = set(rucksacks[i + 2])
        duplicate = a.intersection(b).intersection(c).pop()
        total += get_priority(duplicate)

    return total


if __name__ == "__main__":
    rucksacks = read_input()

    print("part a:", part_a(rucksacks))
    print("part b:", part_b(rucksacks))
