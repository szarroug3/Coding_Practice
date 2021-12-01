# !/bin/python3
# http://www.adventofcode.com/2017/day/5

from utils import read_input
from copy import copy


def get_num_jumps_a(jump_list):
    i = 0
    num_jumps = 0

    while i in jump_list.keys():
        jump = jump_list[i]
        jump_list[i] += 1
        i += jump
        num_jumps += 1

    return num_jumps


def get_num_jumps_b(jump_list):
    i = 0
    num_jumps = 0

    while i in jump_list.keys():
        jump = jump_list[i]
        if jump > 2:
            jump_list[i] -= 1
        else:
            jump_list[i] += 1
        i += jump
        num_jumps += 1

    return num_jumps


JUMP_LIST = {i: value for i, value in enumerate(read_input(val_type=int))}
print('part a:', get_num_jumps_a(copy(JUMP_LIST)))
print('part b:', get_num_jumps_b(JUMP_LIST))
