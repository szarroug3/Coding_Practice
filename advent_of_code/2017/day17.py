# !/bin/python3
# http://www.adventofcode.com/2017/day/17

from collections import deque
from utils import read_input


def spinlock(skip, stop_val=2017, search_val=2017):
    c_buffer = deque([0])

    for i in range(1, stop_val + 1):
        c_buffer.rotate(-skip-1)
        c_buffer.insert(0, i)
    return c_buffer[(c_buffer.index(search_val) + 1) % len(c_buffer)]


if __name__ == '__main__':
    SKIP = read_input(val_type=int)
    print('part a:', spinlock(SKIP))
    print('part b:', spinlock(SKIP, stop_val=50000000, search_val=0))
