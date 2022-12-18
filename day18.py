from helper.input import read_input
import sys
from collections import defaultdict


def is_neighbor(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) == 1


def number_of_sides(input):
    sides = 0
    neighbors = defaultdict(int)
    
    for [x, y, z] in read_input(18, input, [(int,)]):
        p1 = (x, y, z)
        neighbors[p1] = 0
        for p2 in neighbors:
            if is_neighbor(p1, p2):
                neighbors[p1] += 1
                neighbors[p2] += 1
    return len(neighbors) * 6 - sum(neighbors.values())


def part1(input):
    return number_of_sides(input)


def part2(input):
    pass


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
