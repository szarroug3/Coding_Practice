# !/bin/python3
# http://www.adventofcode.com/2017/day/13

from utils import read_input


def create_firewall(info):
    return {d: r for d, r in info}


def get_scanner_pos(time, scanner_range):
    period = scanner_range - 1
    time = time - period
    return abs(period - time % (period * 2))


def get_severity(firewall, delay=0, return_caught=False):
    severity = 0
    for level in range(max(firewall.keys()) + 1):
        if level in firewall and get_scanner_pos(level + delay, firewall[level]) == 0:
            severity += level * firewall[level]
            if return_caught:
                return True
    if return_caught:
        return False
    return severity


def dont_get_caught(firewall):
    delay = 1
    while True:
        if not get_severity(firewall, delay=delay, return_caught=True):
            return delay
        delay += 1


FIREWALL = create_firewall(read_input(val_type=int, separator=': '))
print('part a:', get_severity(FIREWALL))
print('part b:', dont_get_caught(FIREWALL))
