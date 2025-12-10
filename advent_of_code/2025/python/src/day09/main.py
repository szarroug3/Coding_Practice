# !/bin/python3

import time
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
from src.utils import read_input


def process_input(data):
    # [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    manual = []
    for line in data:
        end_index = line.index(']')
        goal = line[1:end_index]
        manual.append({
            'goal': goal,
        })
    return manual


def get_areas(points):
    areas = []
    for i, (x1, y1) in enumerate(points[:-1]):
        for x2, y2 in points[i+1:]:
            areas.append({
                'area': int((math.fabs(x2-x1) + 1) * (math.fabs(y2-y1) + 1)),
                'point_a': (x1, y1),
                'point_b': (x2, y2)
            })
    return sorted(areas, key=lambda a: a['area'], reverse=True)


def part_a(areas):
    sorted_areas = sorted(areas, key=lambda a: a['area'], reverse=True)
    return sorted_areas[0]['area']


def get_edges_and_lines(points):
    edges = {'x': {}, 'y': {}}
    horizontal_lines = {}
    vertical_lines = {}
    length = len(points)
    for i, (x1, y1) in enumerate(points):
        j = (i + 1) % length
        x2, y2 = points[j]
        if x1 == x2:
            if x1 not in edges:
                edges['x'][x1] = []
            edges['x'][x1].append(sorted([y1, y2]))
            if x1 not in vertical_lines:
                vertical_lines[x1] = []
            start, end = sorted([y1, y2])
            for y in range(start, end+1):
                vertical_lines[x1].append(y)
        if y1 == y2:
            if y1 not in edges['y']:
                edges['y'][y1] = []
            if y1 not in horizontal_lines:
                horizontal_lines[y1] = []
            start, end = sorted([x1, x2])
            edges['y'][y1].append([start, end])
            for x in range(start, end+1):
                horizontal_lines[y1].append(x)

    return edges, horizontal_lines, vertical_lines


def is_inside(edges, sorted_x_values, horizontal_lines, vertical_lines, x, y):
    if x in vertical_lines and y in vertical_lines[x]:
        return True
    if y in horizontal_lines and x in horizontal_lines[y]:
        return True

    count = 0
    stuff = []
    for x_edge in sorted_x_values:
        if x_edge < x:
            continue
        for y1, y2 in edges['x'][x_edge]:
            if y1 <= y and y <= y2:
                if x == x_edge:
                    return True
                stuff.append([x_edge, x, y, y1, y2])
                count += 1
                break

    # get horizontal lines that are on the same y as the point we're checking
    # if we find any lines, we need to reduce our count by 1 for each line since they'd
    # be caught as 2 vertices
    if y in edges['y']:
        for x1, _ in edges['y'][y]:
            if x1 > x:
                count -= 1

    return count % 2 != 0


def is_full_rectangle_inside(edges, sorted_x_values, horizontal_lines, vertical_lines, min_x, max_x, min_y, max_y, inside, outside):
    for i, x in enumerate(range(min_x, max_x+1)):
        # print('x', i, '/', max_x+1-min_x)
        for y in range(min_y, max_y+1):
            # was this point cached already?
            if x in inside and y in inside[x]:
                continue
            if x in outside and y in inside[x]:
                return False, inside, outside

            # we've never checked this point so check it and cache it
            if not is_inside(edges, sorted_x_values, horizontal_lines, vertical_lines, x, y):
                if x not in outside:
                    outside[x] = []
                outside[x].append(y)
                return False, inside, outside

            if x not in inside:
                inside[x] = []
            inside[x].append(y)
    return True, inside, outside


def get_inside_from_points(points):
    inside = {}
    for x, y in points:
        if x not in inside:
            inside[x] = []
        inside[x].append(y)
    return inside


def any_vertices_in_rectangle(points, min_x, max_x, min_y, max_y):
    for x, y in points:
        # point is inside rectangle
        if min_x < x and x < max_x and min_y < y and y < max_y:
            return True

        # point is outside rectangle
        if x < min_x or x > max_x or y < min_y or y > max_y:
            continue

    return False


def get_all_points(points):
    full = []
    length = len(points)
    for i, (x1, y1) in enumerate(points[:-1]):
        x2, y2 = points[(i + 1) % length]
        if x1 == x2:
            for y in range(y1, y2):
                full.append([x1, y])
        else:
            for x in range(x1, x2):
                full.append([x, y1])
    return full


def check_rectangle(rectangle, all_points, edges, sorted_x_values, horizontal_lines, vertical_lines):
    x1, y1 = rectangle['point_a']
    x2, y2 = rectangle['point_b']
    min_x = min([x1, x2])
    max_x = max([x1, x2])
    min_y = min([y1, y2])
    max_y = max([y1, y2])

    corners = [[x1, y2], [x2, y1]]
    for x, y in corners:
        if not is_inside(edges, sorted_x_values, horizontal_lines, vertical_lines, x, y):
            return False

    if any_vertices_in_rectangle(all_points, min_x, max_x, min_y, max_y):
        return False

    for x in [min_x, max_x]:
        for y in range(min_y, max_y + 1):
            if not is_inside(edges, sorted_x_values, horizontal_lines, vertical_lines, x, y):
                return False

    for y in [min_y, max_y]:
        for x in range(min_x, max_x + 1):
            if not is_inside(edges, sorted_x_values, horizontal_lines, vertical_lines, x, y):
                return False

    return True


def part_b(areas, points, fig=None, ax=None, delay=0):
    edges, horizontal_lines, vertical_lines = get_edges_and_lines(points)
    all_points = get_all_points(points)
    sorted_x_values = sorted(edges['x'].keys())

    for area in areas:
        x1, y1 = area['point_a']
        x2, y2 = area['point_b']

        if fig and ax:
            rect_points = [[x1, y1], [x1, y2], [x2, y2], [x2, y1], [x1, y1]]
            rect_xs, rect_ys = zip(*rect_points)

            line, = ax.plot(rect_xs, rect_ys, color='blue')
            text = ax.text(0.5, -0.1, f"Area: {area['area']}",
                           color='red', fontsize=12, ha='center', va='center', transform=ax.transAxes)

            fig.canvas.draw()
            fig.canvas.flush_events()

        if check_rectangle(area, all_points, edges, sorted_x_values, horizontal_lines, vertical_lines):
            return area['area']

        if fig and ax:
            time.sleep(delay)
            line.remove()
            text.remove()
            fig.canvas.draw()
            fig.canvas.flush_events()


def create_plot_with_polygon(points):
    points.append(points[0])  # repeat the first point to create a closed loop
    xs, ys = zip(*points)  # create tuples of x and y values
    plt.ion()
    fig, ax = plt.subplots()
    ax.plot(xs, ys, color='red')
    plt.show()
    return fig, ax


def main():
    draw = True
    points = process_input(read_input())
    areas = get_areas(points)
    print(part_a(areas))
    if draw:
        fig, ax = create_plot_with_polygon(points)
        delay = 0.1 if len(areas) < 1000 else 0
        print(part_b(areas, points, fig, ax, delay))
    else:
        print(part_b(areas, points))

    if draw:
        plt.ioff()
        plt.show()


main()
