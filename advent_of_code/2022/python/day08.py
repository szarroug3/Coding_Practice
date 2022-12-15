# !/bin/python3
# https://adventofcode.com/2022/day/8

from utils import read_input


def check_visibility(trees, tree, start, end, constant, row=True):
    for i in range(start, end):
        if row and trees[i][constant] >= tree:
            return False
        if not row and trees[constant][i] >= tree:
            return False
    return True


def is_visible(trees, i, j):
    tree = trees[i][j]
    if check_visibility(trees, tree, 0, i, j):
        return True
    if check_visibility(trees, tree, i + 1, len(trees), j):
        return True
    if check_visibility(trees, tree, 0, j, i, row=False):
        return True
    if check_visibility(trees, tree, j + 1, len(trees[i]), i, row=False):
        return True

    return False


def part_a(trees):
    count = (len(trees) * 2) + ((len(trees[0]) - 2) * 2)
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees[i]) - 1):
            if is_visible(trees, i, j):
                count += 1
    return count


def get_score(trees, tree, start, end, constant, reverse=False, row=True):
    step = -1 if reverse else 1
    count = 0
    for i in range(start, end, step):
        count += 1
        if row and trees[i][constant] >= tree:
            return count
        if not row and trees[constant][i] >= tree:
            return count
    return count


def get_scenic_score(trees, i, j):
    score = 1
    tree = trees[i][j]
    score *= get_score(trees, tree, i - 1, -1, j, reverse=True)
    score *= get_score(trees, tree, i + 1, len(trees), j)
    score *= get_score(trees, tree, j - 1, -1, i, reverse=True, row=False)
    score *= get_score(trees, tree, j + 1, len(trees[i]), i, row=False)
    return score


def part_b(trees):
    score = 0
    for i in range(1, len(trees) - 1):
        for j in range(1, len(trees[i]) - 1):
            curr = get_scenic_score(trees, i, j)
            if curr > score:
                score = curr
    return score


if __name__ == "__main__":
    trees = read_input(line_delimiter="", val_type=int)

    print("part a:", part_a(trees))
    print("part b:", part_b(trees))
