from helper.input import read_input_simple
import sys
import itertools
import time


def get_wind(input):
    [line] = read_input_simple(17, input)
    while True:
        for char in line:
            if char == '<':
                yield -1
            elif char =='>':
                yield 1


def get_block():
    blocks = [((0, 0), (1, 0), (2, 0), (3, 0)),\
              ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),\
              ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),\
              ((0, 0), (0, 1), (0, 2), (0, 3)),\
              ((0, 0), (1, 0), (0, 1), (1, 1))]
    while True:
        for block in blocks:
            yield block

def move_block(x, y, dx, dy):
    return x + dx, y + dy


def can_move(block, x, y, dx, dy, game_map):
    x, y = move_block(x, y, dx, dy)
    for bx, by in block:
        if x + bx < 0:
            return False
        elif x + bx >= 7:
            return False
        elif y + by < 0:
            return False
        elif (x + bx, y + by) in game_map:
            return False
    return True


def at_rest(block, x, y, game_map):
    for bx, by in block:
        if y + by - 1 < 0:
            return True
        elif (x + bx, y + by - 1) in game_map:
            return True
    return False


def print_map(game_map, height, only_top=-1):
    miny = -1 if only_top == -1 else height - only_top
    for y in range(height + 1, miny, -1):
        print('|' + ''.join(['#' if (x, y) in game_map else ' ' for x in range(7)]) + '|')
    print('+-------+')


def part1(input):
    height = 0
    game_map = set()
    wind_generator = get_wind(input)

    for block in itertools.islice(get_block(), 2022):
        x, y = 2, height + 3
        while True:
            wind = next(wind_generator)
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
            else:
                for bx, by in block:
                    game_map.add((x + bx, y + by))
                break
        height = max(height, max((y + by + 1 for _, by in block)))
    return height


def part2(input):
    height = 0
    game_map = set()
    input_length = sum(len(line) for line in read_input_simple(17, input))
    wind_generator = enumerate(get_wind(input))
    cycle_length = input_length * 5

    done = False
    first_height, cycle_height, first_blocks, cycle_blocks = 0, 0, 0, 0
    for block_index, block in enumerate(get_block()):
        x, y = 2, height + 3
        while True:
            j, wind = next(wind_generator)
            if j == cycle_length:
                print_map(game_map, height, 10)
                first_height = height
                first_blocks = block_index
            elif j == cycle_length * 2:
                print_map(game_map, height, 10)
                cycle_height = height - first_height
                cycle_blocks = block_index - first_blocks
                done = True
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
            else:
                for bx, by in block:
                    game_map.add((x + bx, y + by))
                break
        height = max(height, max((y + by + 1 for _, by in block)))
        if done:
            break
    full_cycles_needed = (1000000000000 - first_blocks) // cycle_blocks
    blocks_remaining = (1000000000000 - first_blocks) % cycle_blocks

    second_start_height = height

    for block in itertools.islice(get_block(), blocks_remaining):
        x, y = 2, height + 3
        while True:
            _, wind = next(wind_generator)
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
            else:
                for bx, by in block:
                    game_map.add((x + bx, y + by))
                break
        height = max(height, max((y + by + 1 for _, by in block)))
    print(height - second_start_height, height)

    return first_height + cycle_height * full_cycles_needed + height - second_start_height


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
