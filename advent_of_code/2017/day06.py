# !/bin/python3
# http://www.adventofcode.com/2017/day/4

from math import ceil
from utils import read_input


def redistribute(banks):
    num_loops = 0
    bank_states = [list(banks.values())]

    while True:
        num_loops += 1
        value_index, value = grab_largest(banks)
        distribution_value = ceil(value / len(banks))
        for i in range(value_index + 1, len(banks) + value_index + 1):
            i %= len(banks)
            if value < distribution_value:
                distribution_value = value
            banks[i] += distribution_value
            value -= distribution_value

        seen_index = seen_before(list(banks.values()), bank_states)
        if seen_index:
            return num_loops, num_loops - seen_index

        bank_states.append(list(banks.values()))


def grab_largest(banks):
    value_index = 0
    value = banks[value_index]

    for i in range(1, len(banks)):
        if banks[i] > value:
            value_index = i
            value = banks[i]

    banks[value_index] = 0
    return value_index, value


def seen_before(state, seen):
    for i, s in enumerate(seen):
        found = True
        for j in range(len(state)):
            if s[j] != state[j]:
                found = False
                break
        if found:
            return i
    return


BANKS = {i: value for i, value in enumerate(read_input(separator='\t', val_type=int))}
num_loops, seen_distance = redistribute(BANKS)
print('part a:', num_loops)
print('part b:', seen_distance)
