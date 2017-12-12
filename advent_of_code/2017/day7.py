# !/bin/python3
# http://www.adventofcode.com/2017/day/7

from utils import read_input


def parse_input(tower_info):
    for info in tower_info:
        info = info.split()
        subtowers = []

        # get basic info
        name = info.pop(0)
        weight = int(info.pop(0)[1:-1])

        # if we have more info, get rid of -> and process rest
        if info:
            info.pop(0)
            for subtower in info:
                subtower = subtower.replace(',', '')
                subtowers.append(subtower)

        yield name, weight, subtowers


def process_input(tower_info):
    return {n: {'weight': w, 'subtowers': s} for n, w, s in tower_info}


def find_tower_base(tower_info):
    subtowers = []
    for tower in tower_info.values():
        for subtower in tower['subtowers']:
            subtowers.append(subtower)

    for tower in tower_info:
        if tower not in subtowers:
            return tower


def traverse_tower(tower_info, name):
    for subtower in tower_info[name]['subtowers']:
        if not tower_info[subtower]['subtowers']:
            continue
        yield from traverse_tower(tower_info, subtower)
    for subtower in tower_info[name]['subtowers']:
        if tower_info[subtower]['subtowers']:
            continue
        yield subtower
    yield name


def check_weights(tower_info, subtower):
    if len(tower_info[subtower]['subtowers']) < 3:
        return

    weights = {}
    weight_list = []
    weight_set = set()

    for tower in tower_info[subtower]['subtowers']:
        weight = 0
        for t in traverse_tower(tower_info, tower):
            weight += tower_info[t]['weight']

        weights[tower] = weight
        weight_list.append(weight)
        weight_set.add(weight)

    if len(weight_set) == 1:
        return

    good_weight = None
    bad_weight = None
    bad_tower = None

    for tower, weight in weights.items():
        if weight_list.count(weight) > 1:
            good_weight = weight
        else:
            bad_weight = weight
            bad_tower = tower
        if good_weight and bad_weight:
            break

    return tower_info[bad_tower]['weight'] - bad_weight + good_weight


def find_fixed_weight(tower_info, tower_base):
    for subtower in traverse_tower(tower_info, tower_base):
        fixed_weight = check_weights(tower_info, subtower)
        if fixed_weight:
            return fixed_weight


TOWER_INFO = process_input([T for T in parse_input(read_input())])
TOWER_BASE = find_tower_base(TOWER_INFO)
print('part a:', TOWER_BASE)
print('part b:', find_fixed_weight(TOWER_INFO, TOWER_BASE))
