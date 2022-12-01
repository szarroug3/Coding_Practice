# !/bin/python3
# https://adventofcode.com/2022/day/1

from utils import read_input


def parse(data):
    elves = []
    curr = []
    for line in data:
        if line == '':
            elves.append(curr)
            curr = []
            continue
        curr.append(int(line))
    elves.append(curr)

    return elves


def get_totals(elves):
    totals = []
    for elf in elves:
        totals.append(sum(elf))
    return totals


def part_a(elves):
    return max(elves)


def part_b(elves):
    elves = sorted(elves, reverse=True)
    return sum(elves[:3])


if __name__ == '__main__':
    elves = parse(read_input())
    totals = get_totals(elves)

    print('part a:', part_a(totals))
    print('part b:', part_b(totals))
