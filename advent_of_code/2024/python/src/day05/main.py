# !/bin/python3

from collections import defaultdict
from src.utils import read_input


def process_input(data):
    part1 = True
    rules = []
    updates = []

    for line in data:
        if '|' in line:
            rules.append([int(val) for val in line.split('|')])
        else:
            updates.append([int(val) for val in line.split(',')])

    return rules, updates


def check(update, rules):
    for a, b in rules:
        if a not in update or b not in update:
            continue

        found = False
        for i in update:
            if i == a:
                found = True
                break

            if i == b and not found:
                return False

    return True



def part_a(rules, updates):
    sum = 0
    for update in updates:
        if check(update, rules):
            middle = len(update) // 2
            sum += update[middle]
    return sum


def make_rules_dict(rules):
    mapping = defaultdict(list)

    for a, b in rules:
        mapping[b].append(a)
        
    return mapping


def fix(mapping, update):
    fixed = []
    vals = update

    while len(vals):
        for i in vals:
            if i not in mapping:
                fixed.append(i)
                update.remove(i)
                break

            good = True
            for val in mapping[i]:
                if val not in update:
                    continue
                if val not in fixed:
                    good = False
                    break
                
            if good:
                fixed.append(i)
                update.remove(i)
                
            vals = update

    middle = len(fixed) // 2
    return fixed[middle]


def part_b(rules, updates):
    sum = 0
    mapping = make_rules_dict(rules)
    for update in updates:
        if not check(update, rules):
            sum += fix(mapping, update)
    return sum


def main():
    data = read_input()
    rules, updates = process_input(data)
    print(part_a(rules, updates))
    print(part_b(rules, updates))


main()
