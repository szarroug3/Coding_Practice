# !/usr/bin/python3
# https://www.hackerrank.com/challenges/kingdom-division/problem

import sys

def get_indices_that_must_match(city_map):
    one_possibility = []
    two_possibilities = []
    for city in city_map.values():
        if len(city['conns']) == 1:
            one_possibility.append((city['name'], city['conns'][0]['name']))
        if len(city['conns']) == 2:
            two_possibilities.append((city['name'], city['conns'][0]['name'], city['conns'][1]['name']))
    return one_possibility, two_possibilities

def is_valid(combo, city_map, one_possibility, two_possibilities):
    visited = []
    for i, j in one_possibility:
        if combo[i] != combo[j]:
            return False
        visited.append(i)
        visited.append(j)
    for i, j, k in two_possibilities:
        if combo[i] == combo[j]:
            visited.append(i)
            visited.append(j)
            if combo[i] == combo[k]:
                visited.append(k)
        elif combo[i] == combo[k]:
            visited.append(i)
            visited.append(k)
        else:
            return False

    for city, leader in enumerate(combo):
        if city_map[city]['name'] in visited:
            continue
        found = False
        for conn in city_map[city]['conns']:
            if combo[conn['name']] == leader:
                found = True
                break
        if not found:
            return False
    return True


if len(sys.argv) > 1:
    with open(sys.argv[1]) as input_file:
        NUM_CITIES = int(input_file.readline().strip())
        CITY_MAP = {i: {'conns': [], 'name': i} for i in range(NUM_CITIES)}
        for line in input_file:
            CITY_A, CITY_B = [int(x) - 1 for x in line.strip().split(' ')]
            CITY_MAP[CITY_A]['name'] = CITY_A
            CITY_MAP[CITY_A]['conns'].append(CITY_MAP[CITY_B])
            CITY_MAP[CITY_B]['name'] = CITY_B
            CITY_MAP[CITY_B]['conns'].append(CITY_MAP[CITY_A])
else:
    NUM_CITIES = int(input().strip())
    CITY_MAP = {i: {'conns': [], 'name': i} for i in range(NUM_CITIES)}

    while True:
        try:
            CITY_A, CITY_B = [int(x) - 1 for x in input().strip().split(' ')]
            CITY_MAP[CITY_A]['conns'].append(CITY_MAP[CITY_B])
            CITY_MAP[CITY_B]['conns'].append(CITY_MAP[CITY_A])
        except (EOFError, ValueError):
            break

TOTAL = 0
ONE_POSSIBLITY, TWO_POSSIBILITIES = get_indices_that_must_match(CITY_MAP)
for i in range(2 ** NUM_CITIES):
    COMBO = format(i, 'b').zfill(NUM_CITIES)
    if is_valid(COMBO, CITY_MAP, ONE_POSSIBLITY, TWO_POSSIBILITIES):
        TOTAL += 1
print(TOTAL)
