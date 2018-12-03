# !/bin/python3
# https://adventofcode.com/2018/day/1

from utils import read_input


def get_resulting_frequency(frequencies):
    return sum(frequencies)


def get_first_duplicate_frequency(frequencies):
    freqs = {} # using a dict to save cycles
    curr = 0
    while True:
        for freq in frequencies:
            curr += freq
            if curr in freqs:
                return curr
            freqs[curr] = None


if __name__ == '__main__':
    frequencies = read_input(val_type=int)
    print('part a:', get_resulting_frequency(frequencies))
    print('part a:', get_first_duplicate_frequency(frequencies))
