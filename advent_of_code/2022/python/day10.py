# !/bin/python3
# https://adventofcode.com/2022/day/10

from utils import read_input


def convert_values(line):
    if len(line) == 1:
        return [line[0]]
    return line[0], int(line[1])


def noop(x, command, cycle):
    return x, cycle+1


def addx(x, command, cycle):
    return x+command[1], cycle+2


functions = {'noop': noop, 'addx': addx}


def part_a(commands):
    signal_strength = 0
    x = 1
    prev_x = 1
    cycle = 1
    prev_cycle = 1
    prev_mod = 1

    for command in commands:
        x, cycle = functions[command[0]](x, command, cycle)

        mod = cycle % 20 if cycle <= 20 else (cycle - 20) % 40
        if mod == 0:
            signal_strength += x * cycle
        elif mod < prev_mod:
            signal_strength += prev_x * (cycle-mod)

        prev_x = x
        prev_mod = mod
        prev_cycle = cycle
    return signal_strength


def part_b(commands):
    crt = []
    cycle = 0
    prev_cycle = 0
    x = 1
    prev_x = 1

    for command in commands:
        x, cycle = functions[command[0]](x, command, cycle)
        positions = [i % 40 for i in range(prev_cycle, cycle)]

        for pos in positions:
            if pos == 0:
                crt.append('')
            crt[-1] += '#' if prev_x-1 <= pos <= prev_x+1 else '.'

        prev_x = x
        prev_cycle = cycle
    return '\n' + '\n'.join(crt)


if __name__ == '__main__':
    commands = read_input(line_delimiter=' ', val_type=convert_values)

    print('part a:', part_a(commands))
    print('part b:', part_b(commands))
