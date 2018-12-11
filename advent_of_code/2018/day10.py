# !/bin/python3
# https://adventofcode.com/2018/day/10

import re

from utils import read_input


POS_RE = re.compile(r'position=< ?(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>')
DUP_RE = re.compile(r'(\.{2,})')


def get_positions(inp):
    data = []
    for d in inp:
        r = POS_RE.search(d)
        data.append({'px': int(r.group(1)), 'py': int(r.group(2)), 'vx': int(r.group(3)), 'vy': int(r.group(4))})
    return data


def move(data):
    for d in data:
        d['px'] += d['vx']
        d['py'] += d['vy']
    return data


def get_line(vals, min_x, max_x):
    if not vals:
        return '.' * (abs(max_x - min_x) + 1)

    line = ''
    last_x = min_x - 1

    for x in vals:
        line += '.' * (abs(x - last_x - 1))
        line += '#'
        last_x = x

    line += '.' * (abs(max_x - last_x))
    return line


def print_message(data):
    min_x = min(data, key=lambda d: d['px'])['px']
    min_y = min(data, key=lambda d: d['py'])['py']
    max_x = max(data, key=lambda d: d['px'])['px']
    max_y = max(data, key=lambda d: d['py'])['py']

    if abs(max_x - min_x) > 100 or abs(max_y - min_y) > 100:
        return False

    message = []
    for y in range(min_y, max_y + 1):
        vals = sorted(set([d['px'] for d in data if d['py'] == y]))
        message.append(get_line(vals, min_x, max_x))

    print('\n'.join(message))
    return True


def wait(data):
    time = 0
    while True:
        printed = print_message(data)
        data = move(data)
        if printed:
            print('Time:', time)
            input()
        time += 1


if __name__ == '__main__':
    inp = read_input()
    data = get_positions(inp)
    wait(data)
