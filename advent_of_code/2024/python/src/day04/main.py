# !/bin/python3

from src.utils import read_input


def part_a(data):
    count = 0

    # horizontal
    for line in data:
        count += line.count('XMAS')
        count += line.count('SAMX')

    # vertical
    for y in range(len(data) - 3):
        for x in range(len(data[y])):
            word = data[y][x] + data[y + 1][x] + data[y + 2][x] + data[y + 3][x]
            if word == 'XMAS' or word == 'SAMX':
                count += 1

    # diagonal
    for y in range(len(data) - 3):
        for x in range(len(data[y])):
            if x + 3 < len(data[y]):
                word = data[y][x] + data[y + 1][x + 1] + data[y + 2][x + 2] + data[y + 3][x + 3]
                if word == 'XMAS' or word == 'SAMX':
                    count += 1

            if x >= 3:
                word = data[y][x] + data[y + 1][x - 1] + data[y + 2][x - 2] + data[y + 3][x - 3]
                if word == 'XMAS' or word == 'SAMX':
                    count += 1
                
    return count


def part_b(data):
    count = 0
    for y in range(1, len(data) - 1):
        for x in range(1, len(data[y]) - 1):
            if data[y][x] != 'A':
                continue
            if not (data[y-1][x-1] == 'S' and data[y+1][x+1] == 'M') and not (data[y-1][x-1] == 'M' and data[y+1][x+1] == 'S'):
                continue
            if not (data[y+1][x-1] == 'S' and data[y-1][x+1] == 'M') and not (data[y+1][x-1] == 'M' and data[y-1][x+1] == 'S'):
                continue
            count += 1
    return count


def main():
    data = read_input()
    print(part_a(data))
    print(part_b(data))


main()
