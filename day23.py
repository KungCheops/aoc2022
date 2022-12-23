from helper.input import read_input_simple
import sys
from collections import defaultdict


def elf_positions(input):
    for y, line in enumerate(read_input_simple(23, input)):
        for x, char in enumerate(line):
            if char == '#':
                yield x, y


def check_direction(x, y, direction, other_elves):
    direction %= 4
    if direction == 0:
        return not any((x + dx, y - 1) in other_elves for dx in range(-1, 2))
    if direction == 1:
        return not any((x + dx, y + 1) in other_elves for dx in range(-1, 2))
    if direction == 2:
        return not any((x - 1, y + dy) in other_elves for dy in range(-1, 2))
    if direction == 3:
        return not any((x + 1, y + dy) in other_elves for dy in range(-1, 2))


def any_neighbor(x, y, elves):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dx != 0 or dy != 0) and (x + dx, y + dy) in elves:
                return True
    return False


def get_new_position(x, y, direction):
    direction %= 4
    if direction == 0:
        return x, y - 1
    if direction == 1:
        return x, y + 1
    if direction == 2:
        return x - 1, y
    if direction == 3:
        return x + 1, y

# (bounds, old_position, new_position, elves) ?
def update_bounds(bounds, position):
    minx, maxx, miny, maxy = bounds
    x, y = position
    if x < minx:
        minx = x
    if x > maxx:
        maxx = x
    if y < miny:
        miny = y
    if y > maxy:
        maxy = y
    return (minx, maxx, miny, maxy)


def get_bounds(elves):
    minx = min(x for (x, _) in elves)
    maxx = max(x for (x, _) in elves)
    miny = min(y for (_, y) in elves)
    maxy = max(y for (_, y) in elves)
    return (minx, maxx, miny, maxy)
    


def print_map(elves, bounds=None):
    if not bounds:
        bounds = get_bounds(elves)
    for y in range(bounds[2], bounds[3] + 1):
        print(''.join(('#' if (x, y) in elves else '.') for x in range(bounds[0], bounds[1] + 1)))
    print()


def draw_map(elves, bounds=None):
    if not bounds:
        bounds = get_bounds(elves)
    arr = [[(1 if (x, y) in elves else 0) for x in range(bounds[0], bounds[1] + 1)] for y in range(bounds[2], bounds[3] + 1)]
    plt.imshow(np.array(arr), interpolation='nearest')
    plt.show()


def part1(input):
    elves = set(elf_positions(input))
    for turn in range(10):
        # print_map(elves)
        desired_position = defaultdict(set)
        for elf in elves:
            x, y = elf
            newx, newy = x, y
            if any_neighbor(x, y, elves):
                for direction in range(4):
                    if check_direction(x, y, direction + turn, elves):
                        newx, newy = get_new_position(x, y, direction + turn)
                        break
            desired_position[(newx, newy)].add((x, y))
        elves = set()
        for new_position, old_positions in desired_position.items():
            if len(old_positions) > 1:
                for position in old_positions:
                    elves.add(position)
            else:
                elves.add(new_position)
    # print_map(elves, bounds)
    minx, maxx, miny, maxy = get_bounds(elves)
    return (maxx + 1 - minx) * (maxy + 1 - miny) - len(elves)


def part2(input):
    elves = set(elf_positions(input))
    turn = 0
    while True:
        # print_map(elves)
        desired_position = defaultdict(set)
        for elf in elves:
            x, y = elf
            newx, newy = x, y
            if any_neighbor(x, y, elves):
                for direction in range(4):
                    if check_direction(x, y, direction + turn, elves):
                        newx, newy = get_new_position(x, y, direction + turn)
                        break
            desired_position[(newx, newy)].add((x, y))
        turn += 1
        new_elves = set()
        for new_position, old_positions in desired_position.items():
            if len(old_positions) > 1:
                for position in old_positions:
                    new_elves.add(position)
            else:
                new_elves.add(new_position)
        if new_elves == elves:
            break
        else:
            elves = new_elves
    # print_map(elves)
    return turn


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
