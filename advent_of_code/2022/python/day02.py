# !/bin/python3
# https://adventofcode.com/2022/day/2

from utils import read_input


def part_a(strategy):
    points = {
        'A': {
            'X': 4,  # tie
            'Y': 8,  # win
            'Z': 3   # lose
        },
        'B': {
            'X': 1,  # lose
            'Y': 5,  # tie
            'Z': 9   # win
        },
        'C': {
            'X': 7,  # win
            'Y': 2,  # lose
            'Z': 6   # tie
        }
    }

    score = 0
    for theirs, yours in strategy:
        score += points[theirs][yours]
    return score


def part_b(strategy):
    points = {
        'X': {  # lose
            'A': 3,  # rock -> scissors
            'B': 1,  # paper -> rock
            'C': 2  # scissors -> paper
        },
        'Y': {  # tie
            'A': 4,
            'B': 5,
            'C': 6
        },
        'Z': {  # win
            'A': 8,  # rock -> paper
            'B': 9,  # paper -> scissors
            'C': 7  # scissors -> rock
        }
    }

    score = 0
    for theirs, end in strategy:
        score += points[end][theirs]
    return score


if __name__ == '__main__':
    strategy = read_input(line_delimiter=' ')

    print('part a:', part_a(strategy))
    print('part b:', part_b(strategy))
