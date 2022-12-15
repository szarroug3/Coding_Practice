# !/bin/python3
# https://adventofcode.com/2022/day/2

from utils import read_input


def part_a(strategy):
    points = {
        "A": {"X": 4, "Y": 8, "Z": 3},  # tie  # win  # lose
        "B": {"X": 1, "Y": 5, "Z": 9},  # lose  # tie  # win
        "C": {"X": 7, "Y": 2, "Z": 6},  # win  # lose  # tie
    }

    score = 0
    for theirs, yours in strategy:
        score += points[theirs][yours]
    return score


def part_b(strategy):
    points = {
        "X": {  # lose
            "A": 3,  # rock -> scissors
            "B": 1,  # paper -> rock
            "C": 2,  # scissors -> paper
        },
        "Y": {"A": 4, "B": 5, "C": 6},  # tie
        "Z": {  # win
            "A": 8,  # rock -> paper
            "B": 9,  # paper -> scissors
            "C": 7,  # scissors -> rock
        },
    }

    score = 0
    for theirs, end in strategy:
        score += points[end][theirs]
    return score


if __name__ == "__main__":
    strategy = read_input(line_delimiter=" ")

    print("part a:", part_a(strategy))
    print("part b:", part_b(strategy))
