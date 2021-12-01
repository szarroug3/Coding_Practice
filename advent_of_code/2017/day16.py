# !/bin/python3
# http://www.adventofcode.com/2017/day/16

from utils import read_input
from math import log, pow


def get_order(instructions):
    current_order = [x for x in range(16)]
    order = []
    for instruction in instructions:
        if instruction[0] == 's':
            num = int(instruction[1:])
            current_order = current_order[0 - num:] + current_order[:len(current_order) - num]
            continue

        if instruction[0] == 'x':
            index_a = int(instruction[1:instruction.index('/')])
            index_b = int(instruction[instruction.index('/') + 1:])
            val = current_order[index_a]
            current_order[index_a] = current_order[index_b]
            current_order[index_b] = val
            continue

        if current_order != sorted(current_order):
            order.append(current_order)
        order.append(instruction)
        current_order = [x for x in range(16)]

    if current_order != sorted(current_order):
        order.append(current_order)
    return order


def dance(string, orders):
    for order in orders:
        if isinstance(order, list):
            string = [string[i] for i in order]
            continue
        loc = string.index(order[1])
        string[string.index(order[-1])] = order[1]
        string[loc] = order[-1]
    return string

def dance_loops(orders, num_loops=1):
    string = [chr(c + 97) for c in range(16)]
    seen = [string]
    for _ in range(num_loops):
        num_loops -= 1
        string = dance(string, orders)
        if string in seen:
            break
        seen.append(string)

    # skip all the repetitive iterations we found above
    for _ in range(num_loops % (len(seen) - seen.index(string))):
        string = dance(string, orders)

    return ''.join(string)



if __name__ == '__main__':
    ORDERS = get_order([INSTRUCTION for INSTRUCTION in read_input(separator=',')])
    print('part a:', ''.join(dance_loops(ORDERS)))
    print('part b:', ''.join(dance_loops(ORDERS, num_loops=1000000000)))
