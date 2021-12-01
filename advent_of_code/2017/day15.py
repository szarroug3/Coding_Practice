# !/bin/python3
# http://www.adventofcode.com/2017/day/15

from utils import read_input

def get_next_num(num, factor, mod_criteria):
    while True:
        num = (num * factor) % 2147483647
        if not mod_criteria:
            return num
        if num % mod_criteria == 0:
            return num


def get_match_count(num_a, num_b, mod_criteria=False):
    matches = 0
    if mod_criteria:
        num_pairs = 5000000
        mod_a = 4
        mod_b = 8
    else:
        num_pairs = 40000000
        mod_a = None
        mod_b = None

    for _ in range(num_pairs):
        num_a = get_next_num(num_a, 16807, mod_a)
        num_b = get_next_num(num_b, 48271, mod_b)

        if bin(num_a)[-16:] != bin(num_b)[-16:]:
            continue

        matches += 1
    return matches


if __name__ == '__main__':
    NUM_A, NUM_B = [int(INFO[-1]) for INFO in read_input(separator=' ')]
    print('part a:', get_match_count(NUM_A, NUM_B))
    print('part b:', get_match_count(NUM_A, NUM_B, mod_criteria=True))
