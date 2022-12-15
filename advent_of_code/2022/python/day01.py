# !/bin/python3
# https://adventofcode.com/2022/day/1

from utils import read_input


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


if __name__ == "__main__":
    elves = read_input(
        delimiter="\n\n", line_delimiter="\n", val_type=int, keep_single_item_list=True
    )
    totals = get_totals(elves)

    print("part a:", part_a(totals))
    print("part b:", part_b(totals))
