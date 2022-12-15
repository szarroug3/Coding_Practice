# !/bin/python3
# https://adventofcode.com/2022/day/5

import re
from copy import deepcopy

from utils import read_input


def parse(procedure):
    crate_count = int((len(procedure[0]) + 1) / 4)

    crates = [[] for _ in range(crate_count)]
    movements = []

    crate_pattern = re.compile("(    |[A-Z])")
    move_pattern = re.compile("move (\d+) from (\d+) to (\d+)")

    for line in procedure:
        if line == "" or line[:2] == " 1":
            continue

        if line.startswith("m"):
            match = move_pattern.search(line)
            movements.append(
                [int(match.group(1)), int(match.group(2)) - 1, int(match.group(3)) - 1]
            )
            continue

        match = crate_pattern.findall(line)
        for i, name in enumerate(match):
            if name == "    ":
                continue
            crates[i].insert(0, name)

    return crates, movements


def part_a(crates, movements):
    for count, source, dest in movements:
        for i in range(count):
            crates[dest].append(crates[source].pop())
    return "".join([crate.pop() for crate in crates])


def part_b(crates, movements):
    for count, source, dest in movements:
        crates[dest].extend(crates[source][-count:])
        crates[source] = crates[source][:-count]
    return "".join([crate.pop() for crate in crates])


if __name__ == "__main__":
    crates, movements = parse(read_input(ignore_empty=False, line_ignore_empty=False))

    print("part a:", part_a(deepcopy(crates), movements))
    print("part b:", part_b(deepcopy(crates), movements))
