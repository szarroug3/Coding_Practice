# !/bin/python3
# https://adventofcode.com/2018/day/5


from utils import read_input
from time import sleep


def react(polymer):
    length = -1
    while length != len(polymer):
        length = len(polymer)
        for letter in set(polymer.lower()):
            polymer = polymer.replace(letter + letter.upper(), '').replace(letter.upper() + letter, '')
    return len(polymer)


def remove_problem_child(polymer):
    shortest = len(polymer)
    for letter in set(polymer.lower()):
        shortened = polymer.replace(letter, '').replace(letter.upper(), '')
        reacted = react(shortened)
        if reacted < shortest:
            shortest = reacted
    return shortest
        

if __name__ == '__main__':
    polymer = read_input()
    print('part a:', react(polymer))
    print('part b:', remove_problem_child(polymer))
