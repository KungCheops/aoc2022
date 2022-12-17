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
    wind_generator = enumerate(get_wind(input))
    start_time = time.time_ns()

    for i, block in enumerate(itertools.islice(get_block(), n)):
        if time.time_ns() - start_time >= 1000000000:
            print(f'{100.0*i/n}%')
            start_time += 1000000000
        # print(block)
        x, y = 2, height + 3
        # print(x, y)
        # print(f'Block {block} spawned at point {(x, y)}')
        while True:
            j, wind = next(wind_generator)
            if j % 10091 == 0:
                print_map(game_map, height, 10)
                print(height)
            if can_move(block, x, y, wind, 0, game_map):
                x, y = move_block(x, y, wind, 0)
                # print(f'\tWind pushes block to {(x, y)}')
            # else:
                # print(f'Got pushed into a wall')
            if not at_rest(block, x, y, game_map):
                x, y = move_block(x, y, 0, -1)
                # print(f'\tGravity pushes block to {(x, y)}')
            else:
                # print(f'\tBlock landed at {(x, y)}')
                for bx, by in block:
                    game_map.add((x + bx, y + by))
                break
        height = max(height, max((y + by + 1 for _, by in block)))
        # print_map(game_map, height)
        # print(f'New height: {height}')
        # print()
    return height


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
