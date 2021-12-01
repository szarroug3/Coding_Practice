# !/bin/python3
# https://adventofcode.com/2019/day/5

from utils import read_input


def copy_and_replace(opcodes, noun, verb):
    return opcodes
    new_opcodes = opcodes.copy()
    new_opcodes[1] = noun
    new_opcodes[2] = verb
    return new_opcodes


def restore_gravity_assist(opcodes):
    opcode_funcs = {'1': (add, 3),
                    '2': (multiply, 3),
                    '3': (save, 1),
                    '4': (output, 1)}

    pos = 0
    while pos < len(opcodes):
        opcode_data = str(opcodes[pos]).zfill(5)
        print('opcode_data:', opcode_data, end=' ')
        code = opcode_data[-1]
        func, num_params = opcode_funcs.get(code, (None, None))
        if not func:
            return opcodes

        parameter_data = opcode_data[-3::-1][:num_params]
        input_params = [opcodes[pos + j] for j in range(1, num_params+1)]
        print('pos:', pos, 'params:', input_params, end=' ')

        values = []
        for val_type, val in zip(parameter_data, input_params):
            print('val_type:', val_type, 'val:', val, end=' ')
            if val_type == '0':
                values.append(int(opcodes[val]))
            elif val_type == '1':
                values.append(int(val))
            else:
                raise Exception('Uhhh wut?')
        opcodes = func(opcodes, *values)
        print(opcodes)
        exit()
        pos += num_params + 1

    return opcodes[0]


def add(opcodes, input_a, input_b, result):
    print('add', input_a, input_b, result)
    opcodes[result] = input_a + input_b
    return opcodes


def multiply(opcodes, input_a, input_b, result):
    print('multiply', input_a, input_b, result)
    opcodes[result] = input_a * input_b
    return opcodes


def save(opcodes, x):
    print('save', x)
    print(x)
    return opcodes


def output(opcodes, x):
    print('output', x)
    opcodes[x] = 1
    return opcodes


def find_output(opcodes):
    for i in range(0, 100):
        for j in range(0, 100):
            computer = restore_gravity_assist(copy_and_replace(opcodes, i, j))
            if computer[0] == 19690720:
                return (100 * i + j)


if __name__ == '__main__':
    opcodes = {pos: val for pos, val in enumerate(read_input(val_type=int, separator=','))}
    
    print('part a:', restore_gravity_assist(copy_and_replace(opcodes, 12, 2))[0])
    # print('part b:', find_output(opcodes))
