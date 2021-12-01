# !/bin/python3
# https://adventofcode.com/2019/day/1

from utils import read_input


def get_fuel_req(mass):
    return int(mass / 3) - 2


def account_for_fuel(mass):
    fuel = 0
    new_fuel = get_fuel_req(mass)
    while new_fuel > 0:
        fuel += new_fuel
        new_fuel = get_fuel_req(new_fuel)

    return fuel
    

if __name__ == '__main__':
    masses = read_input(val_type=int)
    print('part a:', sum([get_fuel_req(mass) for mass in masses]))
    print('part b:', sum([account_for_fuel(mass) for mass in masses]))
