from helper.input import read_input_simple
import sys
from collections import defaultdict
from queue import Queue
import numpy as np
from matplotlib import pyplot as plt


def parse_input(input):
    all_lines = list(read_input_simple(24, input))
    width = len(all_lines[0])
    height = len(all_lines)
    inner_width = width - 2
    inner_height = height - 2

    # Maps (x, y, turn_modulo) -> blocked_at_turns: set()
    blizzard_locations = defaultdict(set)
    start = (0, -1)
    end = (inner_width - 1, inner_height)

    for y, line in enumerate(all_lines[1:-1]):
        for x, char in enumerate(line[1:-1]):
            if char == '^':
                for y2 in range(0, inner_height):
                    blizzard_locations[(x, (y - y2) % inner_height, inner_height)].add(y2)
            elif char == '>':
                for x2 in range(0, inner_width):
                    blizzard_locations[((x + x2) % inner_width, y, inner_width)].add(x2)
            elif char == 'v':
                for y2 in range(0, inner_height):
                    blizzard_locations[(x, (y + y2) % inner_height, inner_height)].add(y2)
            elif char == '<':
                for x2 in range(0, inner_width):
                    blizzard_locations[((x - x2) % inner_width, y, inner_width)].add(x2)

    return start, end, inner_width, inner_height, blizzard_locations


def neighboring_cells(position, width, height, start, end, blizzard_locations, turn):
    x, y = position
    neighbors = []
    for x1, y1 in [(x, y), (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
        if (y1 >= 0 and y1 < height and x1 >= 0 and x1 < width) or (x1, y1) == start or (x1, y1) == end:
            if not turn % width in blizzard_locations[(x1, y1, width)] and not turn % height in blizzard_locations[(x1, y1, height)]:
                neighbors.append((x1, y1))
    return neighbors


def dijkstra(width, height, start, ends, blizzard_locations):
    cycle_time = width * height
    to_visit = Queue()
    initial_state = (start, 0, 0)
    to_visit.put((initial_state, []))
    visited = set()
    visited.add(initial_state)
    
    while not to_visit.empty():
        state, path = to_visit.get()
        position, turn, next_checkpoint = state
        if position == ends[next_checkpoint]:
            next_checkpoint += 1
            if next_checkpoint >= len(ends):
                return path + [position]
        
        for neighbor in neighboring_cells(position, width, height, start, ends[0], blizzard_locations, turn + 1):
            new_state = (neighbor, (turn + 1) % cycle_time, next_checkpoint)
            if not new_state in visited:
                to_visit.put((new_state, path + [position]))
                visited.add(new_state)
    return


def print_map(blizzard_locations, turn, width, height, my_position=None):
    for y in range(-1, height + 1):
        print(''.join(('#' if x == -1 or x == width \
                           or (y == -1 and x != 0) or (y == height and x != width - 1) else \
                       '*' if turn % width in blizzard_locations[(x, y, width)] \
                           or turn % height in blizzard_locations[(x, y, height)] else \
                       'x' if (x, y) == my_position else \
                       '.') for x in range(-1, width + 1)))
    print()


def draw_map(blizzard_locations, turn, width, height, my_position=None, block=False):
    arr = [[(2 if x == -1 or x == width \
               or (y == -1 and x != 0) or (y == height and x != width - 1) else \
             1 if turn % width in blizzard_locations[(x, y, width)] \
               or turn % height in blizzard_locations[(x, y, height)] else \
             3 if (x, y) == my_position else \
             0) for x in range(-1, width + 1)] for y in range(-1, height + 1)]
    plt.imshow(np.array(arr), interpolation='nearest')
    plt.show(block=block)
    plt.pause(0.1)
    plt.clf()


def part1(input):
    start, end, width, height, blizzard_locations = parse_input(input)
    ends = list()
    ends.append(end)
    path = dijkstra(width, height, start, [end], blizzard_locations)
    # for i, pos in enumerate(path):
        # print(i, pos)
        # print_map(blizzard_locations, i, width, height, pos)
    return len(path) - 1


def part2(input):
    start, end, width, height, blizzard_locations = parse_input(input)
    path = dijkstra(width, height, start, [end, start, end], blizzard_locations)
    for i, pos in enumerate(path):
        # print(i, pos)
        # print_map(blizzard_locations, i, width, height, pos)
        draw_map(blizzard_locations, i, width, height, pos)
    draw_map(blizzard_locations, i, width, height, end, block=True)
    return len(path) - 1


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
