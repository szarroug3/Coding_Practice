# !/bin/python3
# http://www.adventofcode.com/2017/day/2

from utils import read_input


def get_evenly_divisible_numbers(row):
    for i, val_a in enumerate(row):
        for j, val_b in enumerate(row):
            if i == j:
                continue
            if val_a % val_b == 0:
                return int(val_a / val_b)
            if val_b % val_a == 0:
                return int(val_b / val_a)
    return 0


def get_checksum(rows):
    total_a = 0
    total_b = 0
    for row in rows:
        total_a += max(row) - min(row)
        total_b += get_evenly_divisible_numbers(row)
    return total_a, total_b


ROWS = read_input(val_type=int, separator='\t')
CHECKSUM_A, CHECKSUM_B = get_checksum(ROWS)
print('part a:', CHECKSUM_A)
print('part b:', CHECKSUM_B)
