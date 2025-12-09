# !/bin/python3

from src.utils import read_input


def process_input(data):
    return [list(line) for line in data]


def part_a(data):
    count = 0
    curr = [data[0].index('S')]
    for row in data[1:]:
        beams = set()
        for col in curr:
            if row[col] == '^':
                if col > 0:
                    beams.add(col-1)
                if col < len(row) - 1:
                    beams.add(col + 1)
                count += 1
            else:
                beams.add(col)
        curr = beams
    return count


def part_b(data):
    curr = [0 if val == '.' else 1 for val in data[0]]
    for i, row in enumerate(data[1:]):
        for j in range(len(row)):
            if data[i][j] == '^':
                if j > 0:
                    curr[j - 1] += curr[j]
                if j < len(row) - 1:
                    curr[j + 1] += curr[j]
                curr[j] = 0
    return sum(curr)


def main():
    data = process_input(read_input())
    print(part_a(data))
    print(part_b(data))


main()
