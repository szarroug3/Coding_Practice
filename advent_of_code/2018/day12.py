# !/bin/python3
# https://adventofcode.com/2018/day/12


from utils import read_input


def parse(data):
    plants = {}
    for i, val in enumerate(data[0].split()[-1]):
        plants[int(i)] = val

    notes = {}
    for note in data[2:]:
        d = note.split()
        notes[d[0]] = True if d[-1] == '#' else False

    return plants, notes


def print_plants(plants, gen):
    print('Gen', gen, 'Min', min(plants.keys()), 'Max', max(plants.keys()))
    nums = ''
    p = ''
    for k, v in plants.items():
        nums += str(abs(k))[-1]
        p += v

    print(nums)
    print(p)


def age(plants, notes, gens=20):
    for i in range(gens):
        new_plants = {}
        for j in range(min(plants.keys())-2, max(plants.keys()) + 1):
            combo = ''
            for k in range(j-2, j+3):
                if k not in plants:
                    plants[k] = '.'
                combo += plants[k]

            if notes.get(combo, False):
                new_plants[j] = '#'
            else:
                new_plants[j] = '.'
        plants = new_plants
        print_plants(plants, i+1)
    return plants


def count_plants(plants):
    return sum([k for k, v in plants.items() if v == '#'])


if __name__ == '__main__':
    plants, notes = parse(read_input())
    print_plants(plants, 0)
    print('part a:', count_plants(age(plants, notes)))
