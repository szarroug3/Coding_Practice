# !/bin/python3
# https://adventofcode.com/2022/day/6

from utils import read_input


def find_marker(data, distinct):
    length = len(data)
    for i in range(distinct, length):
        if len(set(data[i-distinct:i])) == distinct:
            return i


if __name__ == '__main__':
    data = read_input()

    print('part a:', find_marker(data, 4))
    print('part b:', find_marker(data, 14))
