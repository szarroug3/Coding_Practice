# !/bin/python3
# http://www.adventofcode.com/2017/day/4

from utils import read_input


def is_valid(passphrase):
    return len(passphrase) == len(set(passphrase))


def is_valid_b(passphrase):
    sorted_passphrases = []
    for phrase in passphrase:
        sorted_passphrases.append(''.join(sorted(list(phrase))))
    return is_valid(sorted_passphrases)


def get_valid_passphrases(passphrases, part='a'):
    if part == 'a':
        return sum([1 for x in passphrases if is_valid(x)])
    else:
        return sum([1 for x in passphrases if is_valid_b(x)])


PASSPHRASES = read_input(separator=' ')
print('part a:', get_valid_passphrases(PASSPHRASES))
print('part a:', get_valid_passphrases(PASSPHRASES, part='b'))
