# !/bin/python3
# https://adventofcode.com/2019/day/2

from utils import read_input


def copy_and_replace(opcodes, noun, verb):
    new_opcodes = opcodes.copy()
    new_opcodes[1] = noun
    new_opcodes[2] = verb
    return new_opcodes


def restore_gravity_assist(opcodes):
    for i in range(0, len(opcodes), 4):
        code = opcodes[i]
        if code == 1:
            func = add
        elif code == 2:
            func = multiply
        else:
            return opcodes

        input_a_pos = opcodes[i + 1]
        input_b_pos = opcodes[i + 2]
        result_pos = opcodes[i + 3]

        input_a_val = opcodes[input_a_pos]
        input_b_val = opcodes[input_b_pos]

        opcodes[result_pos] = func(input_a_val, input_b_val)

    return opcodes[0]


def add(x, y):
    return x + y


def multiply(x, y):
    return x * y


def find_output(opcodes):
    for i in range(0, 100):
        for j in range(0, 100):
            computer = restore_gravity_assist(copy_and_replace(opcodes, i, j))
            if computer[0] == 19690720:
                return (100 * i + j)


if __name__ == '__main__':
    opcodes = {pos: val for pos, val in enumerate(read_input(val_type=int, separator=','))}
    
    print('part a:', restore_gravity_assist(copy_and_replace(opcodes, 12, 2))[0])
    print('part b:', find_output(opcodes))
