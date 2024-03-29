# !/bin/python3
# http://www.adventofcode.com/2017/day/1

from utils import read_input


def get_total(captcha, offset):
    total = 0
    length = len(captcha)
    for i in range(length):
        j = (i + offset) % length
        if captcha[i] == captcha[j]:
            total += int(captcha[i])
    return total


CAPTCHA = read_input()
print('part a:', get_total(CAPTCHA, 1))
print('part b:', get_total(CAPTCHA, int(len(CAPTCHA) / 2)))
