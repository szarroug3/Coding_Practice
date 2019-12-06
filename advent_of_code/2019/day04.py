# !/bin/python3
# https://adventofcode.com/2019/day/4

from utils import read_input


def get_password(min_val, max_val, adjacency_rule=False):
    count = 0
    for val in range(min_val, max_val+1):
        last_digit = int(str(val)[0])
        adjacent = False
        adjacent_count = 1
        increasing = True
        for digit in str(val)[1:]:
            digit = int(digit)
            if digit < last_digit:
                increasing = False
                break

            if last_digit == digit:
                adjacent_count += 1
            else:
                if adjacent_count == 2:
                    adjacent = True
                adjacent_count = 1

            last_digit = digit

        if adjacency_rule and adjacent_count == 2:
            adjacent = True

        if adjacent and increasing:
            count += 1

    return count


if __name__ == '__main__':
    min_val, max_val = read_input(val_type=int, separator='-')
    print('part a:', get_password(min_val, max_val))
    print('part b:', get_password(min_val, max_val, adjacency_rule=True))
