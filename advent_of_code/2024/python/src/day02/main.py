# !/bin/python3

from src.utils import read_input


def check(line):
    if not len(set(line)) == len(line):
        return False

    increasing = line[1] - line[0] > 0

    for i in range(1, len(line)):
        diff = line[i] - line[i-1]

        if abs(diff) > 3:
            return False

        if (diff > 0) != increasing:
            return False

    return True


def part_a(data):
    sum = 0
    for line in data:
        if check(line):
            sum += 1

    return sum


def remove_indices(data, indices):
    for index in indices:
        yield data[0: index] + data[index + 1: len(data)]


def remove_and_check(data, indices):
    for values in remove_indices(data, indices):
        if check(values):
            return True
    return False


def part_b(data):
    sum = 0
    for line in data:
        increasing_count = 0
        decreasing_count = 0

        for i in range(1, len(line)):
            diff = line[i] - line[i-1]
            if diff > 0:
                increasing_count += 1
            elif diff < 0:
                decreasing_count += 1

        increasing = increasing_count > 1
        unsafe_indices = set()

        for i in range(1, len(line)):
            diff = line[i] - line[i-1]
            if abs(diff) > 3 or diff == 0 or (diff > 0) != increasing:
                unsafe_indices.update([i-1, i])

        if (len(unsafe_indices)) == 0:
            sum += 1
        elif remove_and_check(line, unsafe_indices):
            sum += 1

    return sum


def main():
    data = read_input(val_type=int, line_delimiter=' ')
    print(part_a(data))
    print(part_b(data))


main()
