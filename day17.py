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


def print_map(game_map, height, only_top=10):
    miny = -1 if only_top == -1 else height - only_top
    for y in range(height + 1, miny, -1):
        print('|' + ''.join([str(game_map[(x, y)]) if (x, y) in game_map else ' ' for x in range(7)]) + '|')
    print('+-------+')


def part1(input):
    height = 0
    game_map = dict()
    wind_generator = get_wind(input)

    for i, block in enumerate(itertools.islice(get_block(), 2022)):
        x, y = 2, height + 3
        while True:
            wind = next(wind_generator)
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
            else:
                for bx, by in block:
                    game_map[(x + bx, y + by)] = i % 10
                break
        height = max(height, max((y + by + 1 for _, by in block)))
    print_map(game_map, height)
    return height


def part2(input):
    height = 0
    game_map = dict()
    input_length = sum(len(line) for line in read_input_simple(17, input))
    wind_generator = enumerate(get_wind(input))
    block_generator = get_block()
    cycle_length = input_length * 5
    total_blocks_to_drop = 1000000000000

    done = False
    first_height, cycle_height, first_blocks, cycle_blocks, total_blocks_dropped = 0, 0, 0, 0, 0
    for block_index, block in enumerate(block_generator):
        x, y = (2, height + 3)
        while True:
            j, wind = next(wind_generator)
            if j == cycle_length:
                print_map(game_map, height)
                first_height = height
                first_blocks = block_index
            elif j == cycle_length * 2:
                cycle_height = height - first_height
                cycle_blocks = block_index - first_blocks
                total_blocks_dropped = block_index + 1
                done = True
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
            else:
                for bx, by in block:
                    game_map[(x + bx, y + by)] = block_index % 10
                break
        height = max(height, max((y + by + 1 for _, by in block)))
        if done:
            break
    full_cycles_needed = (total_blocks_to_drop - total_blocks_dropped) // cycle_blocks
    blocks_remaining = (total_blocks_to_drop - total_blocks_dropped) % cycle_blocks
    print_map(game_map, height)

    print(f'Summary:\n\tTotal blocks to drop: {total_blocks_to_drop}\n\tBlocks dropped: {total_blocks_dropped}\n\tBlocks dropped per cycle: {cycle_blocks}\n\tFull cycles needed: {full_cycles_needed}\n\tBlocks remaining: {blocks_remaining}\n\tHeight gained per cycle: {cycle_height}\n\tHeight before looping: {height}')

    second_start_height = height

    for i, block in enumerate(itertools.islice(block_generator, blocks_remaining)):
        x, y = 2, height + 3
        while True:
            _, wind = next(wind_generator)
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
            else:
                for bx, by in block:
                    game_map[(x + bx, y + by)] = i % 10
                break
        height = max(height, max((y + by + 1 for _, by in block)))

    print(f'\tHeight after looping: {height}')

    print_map(game_map, height)
    print(height - second_start_height, height)

    return cycle_height * full_cycles_needed + height


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
