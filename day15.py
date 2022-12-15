from helper.input import read_input_simple
import sys


def parse_input(input):
    sensors = []
    for line in read_input_simple(15, input):
        line = line.split(' ')
        x1 = int(line[2][2:-1])
        y1 = int(line[3][2:-1])
        x2 = int(line[8][2:-1])
        y2 = int(line[9][2:])
        sensors.append((x1, y1, x2, y2))
    return sensors


def part1(input):
    sensors = parse_input(input)
    y_cutoff = 10
    y_cutoff = 2000000
    cant_contain = set()
    for sx, sy, bx, by in sensors:
        # print(f'Sensor at ({sx}, {sy}) with beacon at ({bx}, {by})')
        d_sb = abs(sx - bx) + abs(sy - by)
        d_sl = abs(sy - y_cutoff)
        diff = d_sb - d_sl
        if diff >= 0:
            for x in range(sx - diff, sx + diff + 1):
                # print(f'Rules out ({x}, {y_cutoff})')
                cant_contain.add(x)
                # print('New size:', len(cant_contain))
    for sx, sy, bx, by in sensors:
        if sy == y_cutoff and sx in cant_contain:
            cant_contain.remove(sx)
        if by == y_cutoff and bx in cant_contain:
            cant_contain.remove(bx)
    # print(cant_contain)
    return len(cant_contain)


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
