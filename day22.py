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
        match dx, dy:
            case 1, 0:
                return 0, 1
            case 0, 1:
                return -1, 0
            case -1, 0:
                return 0, -1
            case 0, -1:
                return 1, 0
    if direction == 'L':
        match dx, dy:
            case 1, 0:
                return 0, -1
            case 0, -1:
                return -1, 0
            case -1, 0:
                return 0, 1
            case 0, 1:
                return 1, 0


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


#                  Nor, Eas, Sou, Wes
neighbors = {'U': ['F', 'R', 'N', 'L'],\
             'N': ['U', 'R', 'D', 'L'],\
             'R': ['U', 'F', 'D', 'N'],\
             'F': ['U', 'L', 'D', 'R'],\
             'L': ['U', 'N', 'D', 'F'],\
             'D': ['N', 'R', 'F', 'L']}


def rotate(dx, dy, rotation):
    if rotation == 0:
        return dx, dy
    if rotation == 1:
        return turn(dx, dy, 'R')
    if rotation == 3:
        return turn(dx, dy, 'L')
    if rotation == 2:
        dx1, dx2 = turn(dx, dy, 'R')
        return turn(dx1, dx2, 'R')


def neighboring_sides(side, sides, rotation):
    print('Neighbors of', side, rotation)
    index, letter = side
    x, y = index
    for i, (dx, dy) in enumerate([rotate(dx, dy, rotation) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]]):
        # print(x, dx, y, dy, x + dx, y + dy)
        if (x + dx, y + dy) in sides:
            print(f'\t{x + dx}, {y + dy}, {neighbors[letter][i]}')
            yield x + dx, y + dy, neighbors[letter][i]


def get_rotation(side1, side2):
    match (side1, side2):
        case ('U', 'R'):
            return -1
        case ('U', 'N'):
            return 0
        case ('U', 'L'):
            return 1
        case ('U', 'F'):
            return 2
        case ('R', 'F'):
            return 0
        case ('R', 'N'):
            return 0
        case ('R', 'D'):
            return -1
        case ('L', 'N'):
            return 0
        case ('L', 'F'):
            return 0
        case ('L', 'D'):
            return 1
        case ('N', 'D'):
            return 0
        case ('F', 'D'):
            return 2
    return -get_rotation(side2, side1)


def move2(x, y, dx, dy, d, side_letter, sides):
    for _ in range(d):
        x += dx
        y += dy
        print(x, y)
        if not (x, y) in sides[side_letter]:
            return x, y, side_letter
            newx, newy = find_on_new_side(x, y, dx, dy, world)
            if world[(newx, newy)] == 1:
                return x - dx, y - dy
            else:
                x, y = newx, newy
        elif side[(x, y)] == 1:
            return x - dx, y - dy, side_letter
    return x, y, side_letter


def parse_input2(input):
    sides = defaultdict(dict)

    line_gen = read_input_simple(22, input, False)

    lines = list(read_input_simple(22, input, False))
    width = max(len(list(line)) for line in lines[:-2])
    height = len(lines) - 2
    size = int(math.sqrt(width * height / 12))

    y = 0
    up = None
    while (line := next(line_gen)) != '':
        for x, c in enumerate(line):
            if c in {'#', '.'}:
                side_index = (x // size, y // size)
                if c == '#':
                    sides[side_index][(x % size, y % size)] = 1
                else:
                    sides[side_index][(x % size, y % size)] = 0
                if not up:
                    up = side_index
        y += 1

    # sides_map: key='U', value=((2, 1), 0)=(side_index, rotation)
    sides_map = dict()
    to_visit = Queue()
    to_visit.put(((up, 'U'), []))
    visited = set()
    visited.add('U')
    while not to_visit.empty():
        current, previous = to_visit.get()
        current_index, current_letter = current

        if not previous:
            rotation = 0
            sides_map[current_letter] = (current_index, rotation)
        else:
            prev_index, prev_letter, prev_rotation = previous
            prev_x, prev_y = prev_index
            rotation = (prev_rotation + get_rotation(prev_letter, current_letter)) % 4
            sides_map[current_letter] = (current_index, rotation)
        for nx, ny, nletter in neighboring_sides(current, sides.keys(), rotation):
            if not nletter in visited:
                to_visit.put((((nx, ny), nletter), (current_index, current_letter, rotation)))
                visited.add(nletter)

    print(sides_map)

    return sides, sides_map, size, parse_instructions(next(line_gen))



def part2(input):
    sides, sides_map, size, instructions = parse_input2(input)
    x, y, rotation = 0, 0, 0
    dx, dy = 1, 0
    side_letter = 'U'
    side_index = sides_map['U']
    
    # test
    move2(0, 0, -1, 0, 1, 'U', sides_map)
    

    for instruction, arg in instructions:
        if instruction == 'turn':
            dx, dy = turn(dx, dy, arg)
        elif instruction == 'forward':
            x, y = move2(x, y, dx, dy, arg, side_letter, sides_map)
    return 1000 * (y + 1) + 4 * (x + 1) + facing(dx, dy)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
