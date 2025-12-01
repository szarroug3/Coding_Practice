# !/bin/python3

import math
from src.utils import read_input


def process_input(data):
    instructions = []

    for line in data:
        direction = line[0]
        steps = int(line[1:])
        instructions.append((direction, steps))

    return instructions


def part_a(instructions):
    curr = 50
    count = 0
    for direction, steps in instructions:
        if direction == 'L':
            curr -= steps
        elif direction == 'R':
            curr += steps

        curr %= 100

        if not curr:
            count += 1
    return count


def part_b(instructions):
    curr = 50
    count = 0
    for direction, steps in instructions:
        # if we can make a full circle, add the number of full circles to the count
        count += math.fabs(steps // 100)
        leftover = steps % 100

        if direction == 'L':
            # if we're above 0 and have leftover steps and that would move us below 0, count that as getting to 0 once
            if curr > 0 and curr - leftover <= 0:
                count += 1
            curr -= leftover
        elif direction == 'R':
            # if we're below 100 and have leftover steps and that would move us above 100, count that as getting to 0 once
            if curr < 100 and curr + leftover >= 100:
                count += 1
            curr += leftover
        curr %= 100
    return int(count)


def main():
    instructions = process_input(read_input())
    print(part_a(instructions))
    print(part_b(instructions))


main()
