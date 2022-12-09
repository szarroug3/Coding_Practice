# !/bin/python3
# https://adventofcode.com/2022/day/9

from collections import defaultdict
from utils import read_input


def convert_values(line):
    return line[0], int(line[1])


def up(row, column):
    return row-1, column


def down(row, column):
    return row+1, column


def left(row, column):
    return row, column-1


def right(row, column):
    return row, column+1


functions = {
    'U': up, 'D': down, 'L': left, 'R': right
}


def follow(h_row, h_column, t_row, t_column):
    funcs = []

    row_distance = t_row - h_row
    col_distance = t_column - h_column
    row_distance_abs = abs(row_distance)
    col_distance_abs = abs(col_distance)

    if row_distance > 1 or (row_distance > 0 and col_distance_abs > 1):
        funcs.append(up)
    if row_distance < -1 or (row_distance < 0 and col_distance_abs > 1):
        funcs.append(down)

    diff = 0 if funcs else 1
    if col_distance > diff:
        funcs.append(left)
    if col_distance < -diff:
        funcs.append(right)

    for f in funcs:
        t_row, t_column = f(t_row, t_column)

    return t_row, t_column


def part_a(movements):
    h_row = 0
    h_column = 0
    t_row = 0
    t_column = 0
    count = 0
    visited = defaultdict(list)

    for direction, steps in movements:
        for _ in range(steps):
            h_row, h_column = functions[direction](h_row, h_column)
            t_row, t_column = follow(h_row, h_column, t_row, t_column)
            if t_column not in visited[t_row]:
                visited[t_row].append(t_column)
                count += 1

    return count


def part_b(movements):
    h_row = 0
    h_column = 0
    coordinates = [(0, 0) for i in range(9)]
    count = 0
    visited = defaultdict(list)

    for direction, steps in movements:
        for step in range(steps):
            h_row, h_column = functions[direction](h_row, h_column)
            prev_row, prev_column = h_row, h_column

            for i in range(9):
                coordinates[i] = follow(prev_row, prev_column, *coordinates[i])
                prev_row, prev_column = coordinates[i]

            if prev_column not in visited[prev_row]:
                visited[prev_row].append(prev_column)
                count += 1

    return count


if __name__ == '__main__':
    movements = read_input(separator=' ', val_type=convert_values)

    print('part a:', part_a(movements))
    print('part b:', part_b(movements))
