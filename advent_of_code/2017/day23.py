# !/bin/python3
# http://www.adventofcode.com/2017/day/23

from utils import read_input
from collections import defaultdict


def get_int(val, registers):
    try:
        return int(val)
    except ValueError:
        return registers[val]


def set(register, val, registers):
    registers[register] = get_int(val, registers)
    registers['pos'] += 1


def sub(register, val, registers):
    registers[register] -= get_int(val, registers)
    registers['pos'] += 1


def mul(register, val, registers):
    registers[register] *= get_int(val, registers)
    registers['pos'] += 1
    registers['mul_count'] += 1


def jnz(register, val, registers):
    if get_int(register, registers) != 0:
        registers['pos'] += get_int(val, registers)
    else:
        registers['pos'] += 1


def parse_instructions(instructions):
    parsed = []
    for instruction in instructions:
        parsed.append((instruction[0], instruction[1:]))
    return parsed


def follow_instructions_a(instructions):
    registers = defaultdict(int)
    registers['pos'] = 0
    registers['mul_count'] = 0

    from time import sleep
    while registers['pos'] < len(instructions):
        instruction = instructions[registers['pos']]
        # print(instruction[0])
        # sleep(1)
        FUNC[instruction[0]](*instruction[1], registers)

    return registers['mul_count']


def follow_instructions_b(instructions):
    h = 0
    b = 109300
    c = b + 17000
    while True:
        f = 1
        d = 2
        while True:
            e = 2
            print(b, d, e, f)
            while True:
                g = (d * e) - b
                if g == 0:
                    f = 0
                e += 1
                g = e - b
                if g == 0:
                    break
            print(b, d, e, f)
            input()
            d += 1
            g = d - b
            if g == 0:
                break
        if f == 0:
            h -= 1
        g = b - c
        if g == 0:
            return h
        b += 17


if __name__ == '__main__':
    FUNC = {'set': set, 'sub': sub, 'mul': mul, 'jnz': jnz}
    INSTRUCTIONS = parse_instructions(read_input(separator=' '))
    print('part a:', follow_instructions_a(INSTRUCTIONS))
    print('part b:', follow_instructions_b(INSTRUCTIONS))
