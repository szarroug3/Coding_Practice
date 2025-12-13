# !/bin/python3

from src.utils import read_input


def process_input(data):
    banks = []

    for line in data:
        banks.append([int(char) for char in line])

    return banks


def part_a(banks):
    sum = 0
    for batteries in banks:
        first = max(batteries[:-1])
        first_index = batteries.index(first)
        second = max(batteries[first_index + 1:])
        sum += int(f'{first}{second}')
    return sum


def part_b(banks):
    sum = 0
    for batteries in banks:
        curr = ''
        for i in range(11, -1, -1):
            biggest = max(batteries[:-i]) if i else max(batteries)
            index = batteries.index(biggest)
            batteries = batteries[index+1:]
            curr += str(biggest)
        sum += int(curr)
    return sum


def main():
    instructions = process_input(read_input())
    print('part a:', part_a(instructions))
    print('part b:', part_b(instructions))


main()
