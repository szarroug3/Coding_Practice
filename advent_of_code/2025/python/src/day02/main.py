# !/bin/python3

import math
from src.utils import read_input


def process_input(data):
    values = []
    ranges = data.split(',')

    for range in ranges:
        start, end = range.split('-')
        values.append((int(start), int(end)))
    return values


def part_a(ranges):
    total = 0
    for start, end in ranges:
        str_start = str(start)
        str_end = str(end)

        half_start = math.ceil(len(str_start) / 2)
        half_end = len(str_end) // 2

        check_start = int('1' + '0' * (half_start - 1))
        check_end = int('1' + '0' * (half_end))

        for check_value in range(check_start, check_end):
            merged = int(str(check_value) * 2)
            if merged >= start and merged <= end:
                total += merged
    return total


def part_b(ranges):
    total = 0
    for start, end in ranges:
        str_start = str(start)
        str_end = str(end)
        start_len = len(str_start)
        end_len = len(str_end)
        values = set()

        for char_length in range(1, (len(str_end) // 2) + 1):
            min_multiples = math.ceil(start_len / char_length)
            max_multiples = end_len // char_length

            min_value = int('1' + '0' * (char_length - 1))
            max_value = int('9' * char_length)

            for char_to_multiply in range(min_value, max_value + 1):
                # don't add single digit values since they can't have duplicates
                if char_length == 1:
                    min_multiples = max(min_multiples, 2)

                for multiplier in range(min_multiples, max_multiples + 1):
                    merged = int(str(char_to_multiply) * multiplier)
                    if merged >= start and merged <= end:
                        values.add(merged)
        total += sum(values)
    return total


def main():
    ranges = process_input(read_input())
    print(part_a(ranges))
    print(part_b(ranges))


main()
