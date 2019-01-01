# !/bin/python3
# https://adventofcode.com/2018/day/12


from utils import read_input


def get_bare_plants(plants):
    offset = plants.find('#')
    return plants[offset:plants.rfind('#') + 1], offset


def parse(data):
    plants, offset = get_bare_plants(data[0].split()[-1])

    notes = {}
    for note in data[2:]:
        d = note.split()
        if d[-1] == '#':
            notes[d[0]] = True

    return plants, offset, notes


def age_plants(plants, notes):
    plants = '....' + plants + '....'
    new_plants = ''
    for i in range(2, len(plants) - 2):
        if plants[i-2:i+3] in notes:
            new_plants += '#'
        else:
            new_plants += '.'
    plants, offset = get_bare_plants(new_plants)
    return plants, offset - 2


def get_offset(first, last, rounds, results):
    offsets = [val['offset'] for val in results.values() if first <= val['index'] <= last]
    return sum(offsets) * rounds


def get_repeat_count(curr_gen, gens, curr_plants, curr_offset, results):
    gens_left = gens - curr_gen

    first_plants = results[curr_plants]
    last_plants = max(results.values(), key=lambda p: p['index'])

    if first_plants == last_plants:
        rounds = gens_left
        remainder = 0
    else:
        round_len = last_plants['index'] - first_plants['index']
        rounds = gens_left // round_len
        remainder = gens_left % round_len
    result_index = first_plants['index'] + remainder

    for val in results.values():
        if val['index'] == result_index:
            result_plants = val
            break

    previous_offset = min([val for val in results.values() if val['plants'] == curr_plants], key=lambda p: p['index'])['offset']
    rounds_offset = last_plants['offset'] - previous_offset
    remainder_offset = result_plants['offset'] - previous_offset
    curr_offset += (rounds_offset * rounds) + (remainder_offset * remainder)

    return sum(i for i, val in enumerate(result_plants['plants'], start=curr_offset) if val == '#')


def age_gens(plants, offset, notes, gens=20):
    results = {}
    for i, _ in enumerate(range(gens), start=1):
        if plants in results:
            return get_repeat_count(i-1, gens, results[plants]['plants'], offset, results)
        new_plants, plant_offset = age_plants(plants, notes)
        offset += plant_offset
        results[plants] = {'index': i, 'plants': new_plants, 'offset': offset}
        plants = new_plants
    return sum([i + offset for i, val in enumerate(plants) if val == '#'])



if __name__ == '__main__':
    plants, offset, notes = parse(read_input())
    print('part a:', age_gens(plants, offset, notes))
    print('part b:', age_gens(plants, offset, notes, gens=50000000000))
