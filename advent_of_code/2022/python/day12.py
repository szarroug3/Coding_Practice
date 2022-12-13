# !/bin/python3
# https://adventofcode.com/2022/day/12

import sys

from collections import defaultdict
from utils import read_input


def parse(heatmap):
    start = None
    end = None
    data = defaultdict(lambda: defaultdict(dict))

    for i, row in enumerate(heatmap):
        for j, value in enumerate(row):
            if value == 'S':
                start = (i, j)
                value = 'a'
            elif value == 'E':
                end = (i, j)
                value = 'z'
            value = ord(value) - 97

            neighbors = []
            if i > 0:
                up = data[(i-1, j)]
                diff = value - up['value']
                if diff <= 1:
                    neighbors.append((i-1, j))
                if -diff <= 1:
                    up['neighbors'].append((i, j))

            if j > 0:
                left = data[(i, j-1)]
                diff = value - left['value']
                if diff <= 1:
                    neighbors.append((i, j-1))
                if -diff <= 1:
                    left['neighbors'].append((i, j))

            data[(i, j)] = {'value': value, 'neighbors': neighbors}

    return data, start, end


def dijkstra(heatmap, start):
    shortest_path = {}
    unvisited = list(heatmap.keys())

    for node in unvisited:
        shortest_path[node] = sys.maxsize
    shortest_path[start] = 0

    while unvisited:
        curr_min_node = None
        for node in unvisited:
            if curr_min_node == None or shortest_path[node] < shortest_path[curr_min_node]:
                curr_min_node = node

        for node in heatmap[curr_min_node]['neighbors']:
            value = shortest_path[curr_min_node] + 1
            if value < shortest_path[node]:
                shortest_path[node] = value

        unvisited.remove(curr_min_node)

    return shortest_path


if __name__ == '__main__':
    heatmap, start, end = parse(read_input(line_delimiter=''))
    shortest_paths = dijkstra(heatmap, end)
    shortest_from_start = shortest_paths[start]
    shortest_overall = min([shortest_paths[node]
                            for node, data in heatmap.items() if data['value'] == 0])

    print('part a:', shortest_from_start)
    print('part b:', shortest_overall)
