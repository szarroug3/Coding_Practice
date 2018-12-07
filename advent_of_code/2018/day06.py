# !/bin/python3
# https://adventofcode.com/2018/day/6


from collections import defaultdict
from utils import read_input


def manhattan(a, b):
    x = a[0] - b[0]
    if x < 0:
        x *= -1
    y = a[1] - b[1]
    if y < 0:
        y *= -1
    return x + y


def find_closest(curr, coords):
    distances = [(c, manhattan(c, curr)) for c in coords]
    closest = sorted(distances, key=lambda d: d[1])
    if closest[0][1] == closest[1][1]:
        return None
    return closest[0][0]


def find_bounds(coords):
    min_x = min(coords, key=lambda l: l[0])[0]
    min_y = min(coords, key=lambda l: l[1])[1]
    max_x = max(coords, key=lambda l: l[0])[0]
    max_y = max(coords, key=lambda l: l[1])[1]
    return min_x, min_y, max_x, max_y


def walk(min_x, min_y, max_x, max_y):
    for x in range(max_x+1):
        for y in range(max_y+1):
            yield x, y
    
    
def get_close_count(coords):
    min_x, min_y, max_x, max_y = find_bounds(coords)
    m = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for x, y in coords:
        m[x][y]['infinite'] = False

    for x, y in walk(min_x, min_y, max_x, max_y):
        closest = find_closest((x, y), coords)

        if not closest:
            continue

        closest_x, closest_y = closest
        if x == min_x or x == max_x or y == min_y or y == max_y:
            m[closest_x][closest_y]['infinite'] = True
            continue

        m[closest[0]][closest[1]]['count'] += 1

    return m


def find_biggest(coords):
    m = get_close_count(coords)
    biggest = 0
    for x in m.values():
        for d in x.values():
            if d['count'] > biggest and not d['infinite']:
                biggest = d['count']
    return biggest


def find_safe(coords, max_dist=10000):
    size = 0
    min_x, min_y, max_x, max_y = find_bounds(coords)
    for x, y in walk(min_x, min_y, max_x, max_y):
        region = 0
        for c in coords:
            region += manhattan((x, y), c)
            if region >= max_dist:
                break
        if region < max_dist:
            size += 1
    return size


if __name__ == '__main__':
    coords = read_input(val_type=int, separator=', ')
    print('part a:', find_biggest(coords))
    print('part b:', find_safe(coords))
