# !/bin/python3
# https://adventofcode.com/2018/day/8

from collections import deque
from utils import read_input


def get_node_data(data, tree={}, curr=0, prefix=''):
    num_children = data.popleft()
    num_metadata = data.popleft()
    tree[curr] = {'children': [], 'metadata': []}

    for child in range(num_children):
        child_name = len(tree)
        tree = get_node_data(data, tree=tree, curr=child_name, prefix=prefix+'    ')
        tree[curr]['children'].append(child_name)

    for child in range(num_metadata):
        tree[curr]['metadata'].append(data.popleft())

    return tree


def get_sum_metadata(tree):
    total = 0
    for node in tree.values():
        total += sum(node['metadata'])
    return total


def get_node_value(tree, node, total=0):
    if  not tree[node]['children']:
        return total + sum(tree[node]['metadata'])

    for metadata in tree[node]['metadata']:
        if metadata == 0:
            continue

        if metadata > len(tree[node]['children']):
            continue

        total += get_node_value(tree, tree[node]['children'][metadata - 1])
    return total


if __name__ == '__main__':
    data = deque(read_input(val_type=int, separator=' '))
    tree = get_node_data(data)
    print('part a:', get_sum_metadata(tree))
    print('part b:', get_node_value(tree, 0))
