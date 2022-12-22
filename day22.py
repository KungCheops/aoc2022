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


#                  Eas, Sou, Wes, Nor
neighbors = {'U': ['R', 'N', 'L', 'F'],\
             'N': ['R', 'D', 'L', 'U'],\
             'R': ['F', 'D', 'N', 'U'],\
             'F': ['L', 'D', 'R', 'U'],\
             'L': ['N', 'D', 'F', 'U'],\
             'D': ['R', 'F', 'L', 'N']}


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


def neighboring_sides(side, sides, rotation):
    # print('Neighbors of', side, rotation)
    index, letter = side
    x, y = index
    for i, (dx, dy) in enumerate([rotate(dx, dy, rotation) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]]):
        # print(x, dx, y, dy, x + dx, y + dy)
        if (x + dx, y + dy) in sides:
            # print(f'\t{x + dx}, {y + dy}, {neighbors[letter][i]}')
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

    # print(sides_map)

    return sides, sides_map, size, parse_instructions(next(line_gen))


# Return x, y, dx, dy, rotation, side_letter
def move2(x, y, dx, dy, rotation, d, side_letter, sides_map, sides):
    if d == 0:
        return x, y, dx, dy, rotation, side_letter
    elif (x + dx, y + dy) in sides[side_letter]:
        if sides[side_letter][(x + dx, x + dy)] == 1:
            return x, y, dx, dy, rotation, side_letter
        else:
            return move2(x + dx, y + dy, dx, dy, rotation, d - 1, side_letter, sides_map, sides)
    else:
        direction = (facing(dx, dy) + rotation) % 4
        # print(direction)
        new_letter = neighbors[side_letter][direction]
        # print(new_letter)
        new_rotation = (rotation - get_rotation(side_letter, new_letter)) % 4
        # print(new_rotation)
        new_side = sides[new_letter]
        # print(new_side)
        
        # print('New side:', sides[new_letter])
        newdx, newdy = rotate(dx, dy, new_rotation)
        # print(newdx, newdy)
        newx, newy = rotate(x, y, new_rotation)
        # print(newx, newy)
        new_side_index, new_side_rotation = sides_map[new_letter]
        # print(sides[new_side_index])
        if sides[new_side_index][(newx, newy)] == 1:
            return x, y, dx, dy, rotation, side_letter
        else:
            return move2(newx, newy, newdx, newdy, new_rotation, d - 1, new_letter, sides_map, sides)


def part2(input):
    sides, sides_map, size, instructions = parse_input2(input)
    x, y, rotation = 0, 0, 0
    dx, dy = 1, 0
    side_letter = 'U'
    side_index = sides_map['U']
    # test
    print(move2(0, 2, -1, 0, 0, 1, 'U', sides_map, sides), (2, 0, 0, 1, 3, 'L'))
    print(move2(3, 2, 1, 0, 0, 1, 'U', sides_map, sides), (0, 2, 0, 1, 3, 'R'))
    
    return
    for instruction, arg in instructions:
        if instruction == 'turn':
            dx, dy = turn(dx, dy, arg)
        elif instruction == 'forward':
            x, y, dx, dy, rotation, side_letter = move2(x, y, dx, dy, rotation, arg, side_letter, sides_map, sides)
    return 1000 * (y + 1) + 4 * (x + 1) + facing(dx, dy)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
