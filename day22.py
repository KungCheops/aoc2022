from helper.input import read_input_simple
import sys
import math
from collections import defaultdict
from queue import Queue


def parse_instructions(instruction_str):
    i = 0
    while i < len(instruction_str):
        c = instruction_str[i]
        match c.isdigit():
            case False:
                yield ('turn', c)
                i += 1
            case True:
                j = i + 1
                while j < len(instruction_str) and instruction_str[j].isdigit():
                    j += 1
                yield ('forward', int(instruction_str[i:j]))
                i = j


def parse_input(input):
    world = dict()

    line_gen = read_input_simple(22, input, False)
    y = 0
    while (line := next(line_gen)) != '':
        for x, c in enumerate(line):
            if c == '#':
                world[(x, y)] = 1
            elif c == '.':
                world[(x, y)] = 0
        y += 1

    return world, parse_instructions(next(line_gen))


def turn(dx, dy, direction):
    if direction == 'R':
        return -dy, dx
    if direction == 'L':
        return dy, -dx


def find_opposite(x, y, dx, dy, world):
    x, y = x - dx, y - dy
    while (x, y) in world:
        x -= dx
        y -= dy
    return x + dx, y + dy


def move(x, y, dx, dy, d, world):
    for _ in range(d):
        x += dx
        y += dy
        if not (x, y) in world:
            newx, newy = find_opposite(x, y, dx, dy, world)
            if world[(newx, newy)] == 1:
                return x - dx, y - dy
            else:
                x, y = newx, newy
        elif world[(x, y)] == 1:
            return x - dx, y - dy
    return x, y


def top_left(world):
    x, y = 0, 0
    while not (x, y) in world:
        x += 1
    return x, y


def facing(dx, dy):
    if dx == 1:
        return 0
    if dy == 1:
        return 1
    if dx == -1:
        return 2
    if dy == -1:
        return 3


def dxdy(facing):
    if facing == 0:
        return 1, 0
    if facing == 1:
        return 0, 1
    if facing == 2:
        return -1, 0
    if facing == 3:
        return 0, -1


def part1(input):
    world, instructions = parse_input(input)
    x, y = top_left(world)
    dx, dy = 1, 0
    for instruction, arg in instructions:
        if instruction == 'turn':
            dx, dy = turn(dx, dy, arg)
        elif instruction == 'forward':
            x, y = move(x, y, dx, dy, arg, world)
    return 1000 * (y + 1) + 4 * (x + 1) + facing(dx, dy)


def rotate(dx, dy, rotation):
    rotation = rotation % 4
    if rotation == 0:
        return dx, dy
    if rotation == 1:
        return turn(dx, dy, 'R')
    if rotation == 3:
        return turn(dx, dy, 'L')
    if rotation == 2:
        dx1, dx2 = turn(dx, dy, 'R')
        return turn(dx1, dx2, 'R')


def parse_input2(input):
    world = dict()

    line_gen = read_input_simple(22, input, False)

    lines = list(read_input_simple(22, input, False))
    width = max(len(list(line)) for line in lines[:-2])
    height = len(lines) - 2
    size = int(math.sqrt(width * height / 12))
    start = None

    y = 0
    while (line := next(line_gen)) != '':
        for x, c in enumerate(line):
            if c in {'#', '.'}:
                side_index = (x // size, y // size)
                position = (x % size, y % size, side_index)
                if c == '#':
                    world[position] = 1
                else:
                    world[position] = 0
                if not start:
                    start = position
        y += 1

    return world, size, start, parse_instructions(next(line_gen))


def get_new_dxdy_and_side(x, y, dx, dy, side_index, size):
    match dx, dy, side_index:
        case 1, 0, (1, 0):
            return 0, y, 1, 0, (2, 0)
        case 0, 1, (1, 0):
            return x, 0, 0, 1, (1, 1)
        case -1, 0, (1, 0):
            return 0, size - y - 1, 1, 0, (0, 2)
        case 0, -1, (1, 0):
            return 0, x, 1, 0, (0, 3)
        case 1, 0, (2, 0):
            return size - 1, size - y - 1, -1, 0, (1, 2)
        case 0, 1, (2, 0):
            return size - 1, x, -1, 0, (1, 1)
        case -1, 0, (2, 0):
            return size - 1, y, -1, 0, (1, 0)
        case 0, -1, (2, 0):
            # maybe wrong?
            return x, size - 1, 0, -1, (0, 3)
        case 1, 0, (1, 1):
            return y, size - 1, 0, -1, (2, 0)
        case 0, 1, (1, 1):
            return x, 0, 0, 1, (1, 2)
        case -1, 0, (1, 1):
            return y, 0, 0, 1, (0, 2)
        case 0, -1, (1, 1):
            return x, size - 1, 0, -1, (1, 0)
        case 1, 0, (0, 2):
            return 0, y, 1, 0, (1, 2)
        case 0, 1, (0, 2):
            return x, 0, 0, 1, (0, 3)
        case -1, 0, (0, 2):
            return 0, size - y - 1, 1, 0, (1, 0)
        case 0, -1, (0, 2):
            return 0, x, 1, 0, (1, 1)
        case 1, 0, (1, 2):
            return size - 1, size - y - 1, -1, 0, (2, 0)
        case 0, 1, (1, 2):
            return size - 1, x, -1, 0, (0, 3)
        case -1, 0, (1, 2):
            return size - 1, y, -1, 0, (0, 2)
        case 0, -1, (1, 2):
            return x, size - 1, 0, -1, (1, 1)
        case 1, 0, (0, 3):
            return y, size - 1, 0, -1, (1, 2)
        case 0, 1, (0, 3):
            return x, 0, 0, 1, (2, 0)
        case -1, 0, (0, 3):
            return y, 0, 0, 1, (1, 0)
        case 0, -1, (0, 3):
            return x, size - 1, 0, -1, (0, 2)


def move2(x, y, side_index, dx, dy, d, world, size):
    if d == 0:
        return x, y, side_index, dx, dy
    elif (x + dx, y + dy, side_index) in world:
        if world[(x + dx, y + dy, side_index)] == 1:
            return x, y, side_index, dx, dy
        else:
            return move2(x + dx, y + dy, side_index, dx, dy, d - 1, world, size)
    else:
        new_x, new_y, new_dx, new_dy, new_side_index = get_new_dxdy_and_side(x, y, dx, dy, side_index, size)

        if world[(new_x, new_y, new_side_index)] == 1:
            return x, y, side_index, dx, dy
        else:
            return move2(new_x, new_y, new_side_index, new_dx, new_dy, d - 1, world, size)


def part2(input):
    world, size, start, instructions = parse_input2(input)
    x, y, side_index = start
    dx, dy = 1, 0

    for instruction, arg in instructions:
        if instruction == 'turn':
            dx, dy = turn(dx, dy, arg)
        elif instruction == 'forward':
            x, y, side_index, dx, dy = move2(x, y, side_index, dx, dy, arg, world, size)
    global_x = x + side_index[0] * size
    global_y = y + side_index[1] * size
    return 1000 * (global_y + 1) + 4 * (global_x + 1) + facing(dx, dy)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
