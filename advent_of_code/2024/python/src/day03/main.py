# !/bin/python3

import re

from src.utils import read_input

PATTERN = re.compile('mul\((\d{1,3}),(\d{1,3})\)')


def get_sum(data):
    sum = 0
    for a, b in re.findall(PATTERN, data):
        sum += int(a) * int(b)
    return sum


def part_a(data):
    return get_sum(data)


def part_b(data):
    sum = 0
    pattern = re.compile("do\(\)(.+?)don't\(\)")

    # get the sum of the values until the first don't
    end = data.find("don't()")
    sum += get_sum(data[:end])

    # get the sum of the values in the middle
    data = data[end:]
    for match in pattern.findall(data):
        sum += get_sum(match)

    # get the sum of the values of the string from the last do onward if it's after the last don't
    # find last don't
    last = data.rfind("don't()")
    data = data[last:]

    # find last do after the last don't
    last = data.rfind("do()")
    data = data[last:] if last != -1 else ''

    sum += get_sum(data)

    return sum


def main():
    data = ''.join(read_input())
    print(part_a(data))
    print(part_b(data))


main()
