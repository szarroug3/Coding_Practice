# !/bin/python3
# https://adventofcode.com/2018/day/4

from collections import Counter, defaultdict
from utils import read_input


def parse_data(data):
    guards = defaultdict(Counter)
    curr_guard = None
    sleep_start = None

    for d in sorted(data):
        minute = int(d[15:17])
        if 'falls asleep' in d:
            sleep_start = minute
        elif 'wakes up' in d:
            for i in range(sleep_start, minute):
                guards[curr_guard][i] += 1
        else:
            curr_guard = int(d.split('#')[1].split(' ')[0])
    return guards


def get_sleepiest(guards):
    data = [(key, sum(val.values())) for key, val in guards.items()]
    return max(data, key=lambda x:x[1])[0]


def get_sleepy(guards):
    sleepy = get_sleepiest(guards)
    sleepy_minute = guards[sleepy].most_common(1)[0][0]
    return sleepy * sleepy_minute


def get_sleepy_minute(guards):
    sleepy = None
    sleepy_minute = None
    sleepy_count = 0

    for guard, data in guards.items():
        sleep = data.most_common(1)[0]
        if sleep[1] > sleepy_count:
            sleepy_count = sleep[1]
            sleepy_minute = sleep[0]
            sleepy = guard
    return sleepy * sleepy_minute



if __name__ == '__main__':
    guards = parse_data(read_input())
    print('part a:', get_sleepy(guards))
    print('part b:', get_sleepy_minute(guards))
