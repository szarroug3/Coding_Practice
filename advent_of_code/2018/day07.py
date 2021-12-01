# !/bin/python3
# https://adventofcode.com/2018/day/7


from collections import defaultdict
from utils import read_input


def get_ready(prerequisites, exclude=[], num=1):
    return sorted([key for key, val in prerequisites.items() if len(val) == 0 if key not in exclude])


def remove(prerequisites, val):
    for values in prerequisites.values():
        if val in values:
            values.remove(val)
    del prerequisites[val]
    return prerequisites


def get_prerequisites(instructions):
    prerequisites = defaultdict(list)
    for i in instructions:
        first = i[1]
        second = i[7]
        prerequisites[second].append(first)
        if first not in prerequisites:
            prerequisites[first] = list()
    return prerequisites


def get_order(prerequisites):
    prerequisites = get_prerequisites(instructions)
    order = ''
    while prerequisites:
        ready = get_ready(prerequisites)[0]
        order += ready
        prerequisites = remove(prerequisites, ready)
    return order


def get_worker(workers):
    for work in workers.values():
        if not work['end']:
            return work


def assign_work(worker, working, base_time, val, curr_time):
    working.append(val)
    worker['val'] = val
    worker['end'] = curr_time + ord(val) - 64 + base_time
    return working

def update_work(prerequisites, workers, working, curr_time):
    for w in workers.values():
        if w['end'] and curr_time >= w['end']:
            prerequisites = remove(prerequisites, w['val'])
            working.remove(w['val'])
            w['val'] = None
            w['end'] = None
    return prerequisites, workers, working

        
def get_time_with_workers(instructions, workers=5, base_time=60):
    prerequisites = get_prerequisites(instructions)
    workers = {x: {'end': None, 'val': None} for x in range(workers)}
    curr_time = -1
    working = []
    while prerequisites:
        curr_time += 1
        prerequisites, workers, working = update_work(prerequisites, workers, working, curr_time)
        for ready in get_ready(prerequisites, exclude=working):
            worker = get_worker(workers)
            if not worker:
                break
            working = assign_work(worker, working, base_time, ready, curr_time)
    return curr_time
        


if __name__ == '__main__':
    instructions = read_input(separator=' ')
    print('part a:', get_order(instructions))
    print('part b:', get_time_with_workers(instructions, workers=5, base_time=60))
