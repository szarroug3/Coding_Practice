# !/bin/python3
# http://www.adventofcode.com/2017/day/18

from time import sleep
from utils import read_input
from collections import defaultdict
from multiprocessing.pool import ThreadPool
from threading import Thread


def get_int(val, registers):
    try:
        return int(val)
    except ValueError:
        return registers[val]


def snd(val, registers):
    registers['last_sound'] = get_int(val, registers)
    registers['pos'] += 1


def set_reg(register, val, registers):
    registers[register] = get_int(val, registers)
    registers['pos'] += 1


def add(register, val, registers):
    registers[register] += get_int(val, registers)
    registers['pos'] += 1


def mul(register, val, registers):
    registers[register] *= get_int(val, registers)
    registers['pos'] += 1


def mod(register, val, registers):
    registers[register] %= get_int(val, registers)
    registers['pos'] += 1


def rcv(register, registers):
    registers['pos'] += 1
    if registers[register] == 0:
        return None
    return registers['last_sound']


def jgz(register, val, registers):
    if registers[register] > 0:
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
    while registers['pos'] < len(instructions):
        instruction = instructions[registers['pos']]
        res = FUNC[instruction[0]](*instruction[1], registers)
        if res:
            return res


def follow_instructions_c(instructions):
    programs = {0: defaultdict(int), 1: defaultdict(int)}

    programs[0].update({'id': 0, 'p': 0, 'pos': 0, 'inbox': [], 'waiting': False})
    programs[1].update({'id': 1, 'p': 1, 'pos': 0, 'inbox': [], 'waiting': False})

    curr = programs[0]
    other = programs[1]
    num_received = 0
    p = False

    while not programs[0]['waiting'] or not programs[1]['waiting']:
        instruction = instructions[curr['pos']]
        if instruction[0] == 'rcv':
            if not curr['inbox']:
                curr['waiting'] = True
                temp = curr
                curr = other
                other = temp
                continue

            curr[instruction[1][0]] = curr['inbox'].pop(0)
            curr['pos'] += 1
            if curr['id'] == 1:
                num_received += 1
            continue

        FUNC[instruction[0]](*instruction[1], curr)
        if instruction[0] == 'snd':
            other['inbox'].append(curr['last_sound'])
            other['waiting'] = False

    return num_received


def wait_for_message(program, other):
    sleep(.001)
    while not program['inbox']:
        program['waiting'] = True
        if other['waiting']:
            return None
    program['waiting'] = False
    return program['inbox'].pop(0)


def program_zero_init(program, other):
    program['p'] = 818478951
    program['a'] = 2147483647
    other['inbox'].append(8951)
    num_received = 0

    for _ in range(126):
        program['p'] *= 8505
        program['p'] %= program['a']
        program['p'] *= 129749
        program['p'] += 12345
        program['p'] %= program['a']
        program['b'] = program['p'] % 10000
        other['inbox'].append(program['b'])

    # wait for a message from other program or deadlock
    val = wait_for_message(program, other)
    if not val:
        return num_received
    num_received += 1

    # wait until we either deadlock or get a positive value from other program
    while val <= 0:
        val = wait_for_message(program, other)
        if not val:
            return num_received
        num_received += 1

    return main_loop(program, other, num_received)


def main_loop(program, other, num_received):
    while True:
        f = 0

        val = wait_for_message(program, other)
        if not val:
            return num_received
        num_received += 1

        # got message
        program['a'] = val

        for _ in range(126):
            val = wait_for_message(program, other)
            if not val:
                return num_received
            num_received += 1

            if val > program['a']:
                other['inbox'].append(val)
                f = 1
            else:
                other['inbox'].append(program['a'])
                program['a'] = val

        other['inbox'].append(program['a'])
        if f > 0:
            continue

        val = wait_for_message(program, other)
        if not val:
            return num_received
        num_received += 1

        while val <= 0:
            val = wait_for_message(program, other)
            if not val:
                return num_received
            num_received += 1

        if program['a'] > 0:
            return num_received


def follow_instructions_b():
    registers_zero = defaultdict(int)
    registers_zero['inbox'] = []
    registers_zero['waiting'] = False

    registers_one = defaultdict(int)
    registers_one['inbox'] = []
    registers_one['waiting'] = False

    registers_zero['id'] = 0
    registers_one['id'] = 1

    pool = ThreadPool(processes=2)
    pool.apply_async(program_zero_init, (registers_zero, registers_one))
    program_one = pool.apply_async(main_loop, (registers_one, registers_zero, 0))

    return program_one.get()


if __name__ == '__main__':
    FUNC = {'snd': snd, 'set': set_reg, 'add': add, 'mul': mul, 'mod': mod, 'rcv': rcv, 'jgz': jgz}
    INSTRUCTIONS = parse_instructions(read_input(separator=' '))
    print('part a:', follow_instructions_a(INSTRUCTIONS))
    print('part b:', follow_instructions_b())
