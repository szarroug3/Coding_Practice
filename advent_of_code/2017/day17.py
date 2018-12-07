# !/bin/python3
# http://www.adventofcode.com/2017/day/17

from utils import read_input


def spinlock(skip, stop_val=2017, search_val=2017):
    c_buffer = [0]
    i = 1
    current_pos = 0

    while i <= stop_val:
        insert_at = ((current_pos + skip) % len(c_buffer)) + 1
        c_buffer.insert(insert_at, i)
        current_pos = insert_at
        i += 1
        if i % SKIP == 0:
            print(c_buffer)
            input()
    return c_buffer[c_buffer.index(search_val) % len(c_buffer) + 1]


if __name__ == '__main__':
    SKIP = read_input(val_type=int)
    print('part a:', spinlock(SKIP))
    print('part b:', spinlock(SKIP, stop_val=50000000, search_val=0))
