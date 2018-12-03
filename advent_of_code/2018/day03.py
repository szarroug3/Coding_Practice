# !/bin/python3
# https://adventofcode.com/2018/day/3

from utils import read_input


def get_claim_slots(x, y, h, w):
    for i in range(x, x + w):
        for j in range(y, y + h):
            yield j, i


def parse_claim(fabric, claim, overlapping, non_overlapping):
    id, _, pos, dim = claim.split()
    id = int(id[1:])
    x, y = pos.split(',')
    x = int(x)
    y = int(y[:-1])
    w, h = [int(d) for d in dim.split('x')]

    non_overlapping.add(id)
    for j, i in get_claim_slots(x, y, h, w):
        if fabric[j][i] is None:
            fabric[j][i] = id
        else:
            if id in non_overlapping:
                non_overlapping.remove(id)

            if isinstance(fabric[j][i], int):
                if fabric[j][i] in non_overlapping:
                    non_overlapping.remove(fabric[j][i])
                overlapping += 1
                fabric[j][i] = '*'

    return overlapping, non_overlapping


def process_claims(claims):
    h = 1000
    w = 1000
    fabric = [[None for _ in range(w)] for _ in range(h)]
    overlapping = 0
    non_overlapping = set()
    for claim in claims:
        overlapping, non_overlapping = parse_claim(fabric, claim, overlapping, non_overlapping)
    return overlapping, non_overlapping


if __name__ == '__main__':
    claims = read_input()
    overlapping, non_overlapping = process_claims(claims)
    print('part a:', overlapping)
    print('part b:', ', '.join([str(x) for x in non_overlapping]))
