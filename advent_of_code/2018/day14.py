# !/bin/python3
# https://adventofcode.com/2018/day/14


from utils import read_input


def make(num_recipes):
    part_a, part_b = None, None
    recipes = [3, 7]
    elf_a = {'recipe': 3, 'pos': 0}
    elf_b = {'recipe': 7, 'pos': 1}
    check_index = 0
    num_recipes_str = str(num_recipes)
    printed = False

    while not part_a or not part_b:
        next_recipes_sum = elf_a['recipe'] + elf_b['recipe']
        next_recipes = str(next_recipes_sum)

        for n in next_recipes:
            recipes.append(int(n))

        elf_a['pos'] = (elf_a['pos'] + elf_a['recipe'] + 1) % len(recipes)
        elf_a['recipe'] = recipes[elf_a['pos']]

        elf_b['pos'] = (elf_b['pos'] + elf_b['recipe'] + 1) % len(recipes)
        elf_b['recipe'] = recipes[elf_b['pos']]

        if not part_a and len(recipes) >= num_recipes + 10:
            part_a = ''.join(str(r) for r in recipes[num_recipes:num_recipes+10])

        if not part_b:
            new = ''.join(str(r) for r in recipes[-len(num_recipes_str)-len(next_recipes)+1:])
            if num_recipes_str in new:
                part_b = len(recipes) - (len(num_recipes_str) - new.index(num_recipes_str) + 1)

    return part_a, part_b


if __name__ == '__main__':
    num_recipes = read_input(val_type=int)
    part_a, part_b = make(num_recipes)
    print('part a:', part_a)
    print('part b:', part_b)
