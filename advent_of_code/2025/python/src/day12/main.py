# !/bin/python3

from src.utils import read_input


def process_input(data):
    shapes = []
    trees = []
    in_shapes = True
    shape = []
    for line in data:
        if 'x' in line:
            in_shapes = False

        if in_shapes:
            if ':' in line:
                continue
            if line == '':
                shapes.append(shape)
                shape = []
                continue
            shape.append(line)
        else:
            if not line:
                continue
            dimensions_end = line.index(':')
            dimensions = [int(val) for val in line[:dimensions_end].split('x')]
            presents = [int(val)
                        for val in line[dimensions_end + 2:].split(' ')]
            trees.append({'dimensions': dimensions, 'presents': presents})

    return {'shapes': shapes, 'trees': trees}


def check(tree, sizes, shapes):
    width, length = tree['dimensions']
    space = width * length

    total = 0
    for i, count in enumerate(tree['presents']):
        if count == 0:
            continue

        total += count * sizes[i]
        if total > space:
            return False

        shape = shapes[i]
        present_width = len(shape[0])
        present_length = len(shape)
        if present_width <= width and present_length <= length:
            continue
        if present_width <= length and present_length <= width:
            continue
        return False
    return True


def part_a(instructions):
    sizes = [
        sum(
            line.count('#') for line in shape
        )
        for shape in instructions['shapes']
    ]

    count = 0
    for tree in instructions['trees']:
        # check for any tom foolery
        if not check(tree, sizes, instructions['shapes']):
            continue
        count += 1

    return 0


def part_b(instructions):
    return 0


def main():
    instructions = process_input(read_input(ignore_empty=False))
    print('part a:', part_a(instructions))
    print('part b:', part_b(instructions))


main()
