from helper.input import read_input
import sys
from collections import defaultdict
import numpy as np


dir_tup = {'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0)}


def add_tup(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return (x1 + x2, y1 + y2)


def get_step(pos, desired_pos):
    (x1, y1) = pos
    (x2, y2) = desired_pos
    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
        return (0, 0)
    dx = int(np.sign(x2 - x1))
    dy = int(np.sign(y2 - y1))
    return (dx, dy)


def part1(input):
    visited = defaultdict(int)
    head_pos = (0, 0)
    tail_pos = (0, 0)
    for direction, length in read_input(9, input, [(str,), (int,)]):
        for _ in range(length):
            head_pos = add_tup(head_pos, dir_tup[direction])
            tail_pos = add_tup(tail_pos, get_step(tail_pos, head_pos))
            visited[tail_pos] = 1
    return len(visited.values())
            


def part2(input):
    visited = defaultdict(int)
    snake_pos = [(0, 0) for _ in range(10)]
    for direction, length in read_input(9, input, [(str,), (int,)]):
        for _ in range(length):
            snake_pos[0] = add_tup(snake_pos[0], dir_tup[direction])
            for i in range(1, len(snake_pos)):
                snake_pos[i] = add_tup(snake_pos[i], get_step(snake_pos[i], snake_pos[i-1]))
            visited[snake_pos[-1]] = 1
    return len(visited.values())


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
