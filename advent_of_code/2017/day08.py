# !/bin/python3
# http://www.adventofcode.com/2017/day/8

from utils import read_input
from collections import defaultdict


def gt(register, value):
    return REGISTERS[register] > value


def ge(register, value):
    return REGISTERS[register] >= value


def lt(register, value):
    return REGISTERS[register] < value


def le(register, value):
    return REGISTERS[register] <= value


def eq(register, value):
    return REGISTERS[register] == value


def ne(register, value):
    return REGISTERS[register] != value


def inc(register, value):
    REGISTERS[register] += value


def dec(register, value):
    REGISTERS[register] -= value


def process_instruction(instruction):
    reg_change, op_change, val_change, _, reg_test, op_test, val_test = instruction
    if FUNCTIONS[op_test](reg_test, int(val_test)):
        FUNCTIONS[op_change](reg_change, int(val_change))


REGISTERS = defaultdict(int)
FUNCTIONS = {'>': gt, '>=': ge, '<': lt, '<=': le, '==': eq, '!=': ne, 'inc': inc, 'dec': dec}
INSTRUCTIONS = read_input(separator=' ')
MAX_VAL = 0
for INSTRUCTION in INSTRUCTIONS:
    process_instruction(INSTRUCTION)
    CURRENT_MAX = max(REGISTERS.values())
    if CURRENT_MAX > MAX_VAL:
        MAX_VAL = CURRENT_MAX
print('part a:', max(REGISTERS.values()))
print('part b:', MAX_VAL)
