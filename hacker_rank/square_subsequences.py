# !/usr/bin/python3
# https://www.hackerrank.com/challenges/square-subsequences/problem

from itertools import combinations


def clean_sequence(sequence):
    clean = ''
    for letter in sequence:
        if sequence.count(letter) > 1:
            clean += letter
    return clean


def is_square_string(sequence):
    length = len(sequence)
    if length % 2 != 0 and length > 1:
        return False

    half = int(len(sequence) / 2)
    if sequence[:half] != sequence[half:]:
        return False

    return True


num_seq = int(input().strip())
for i in range(num_seq):
    sequence = clean_sequence(input().strip())
    total = 0
    for i in range(2, len(sequence) + 1):
        for seq in combinations(sequence, i):
            if is_square_string(''.join(seq)):
                total += 1
    print(total % 1000000007)
