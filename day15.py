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
    # y_cutoff = 10
    y_cutoff = 2000000
    ranges = list()
    for sx, sy, bx, by in sensors:
        # print(f'Sensor at ({sx}, {sy}) with beacon at ({bx}, {by})')
        d_sb = abs(sx - bx) + abs(sy - by)
        d_sl = abs(sy - y_cutoff)
        diff = d_sb - d_sl
        if diff >= 0:
            ranges.append([sx - diff, sx + diff])

    ranges.sort()
    merged_ranges = [ranges[0]]
    for i in range(1, len(ranges)):
        if ranges[i][0] > merged_ranges[-1][1] + 1:
            merged_ranges.append(ranges[i])
        else:
            merged_ranges[-1][1] = max(ranges[i][1], merged_ranges[-1][1])
    return sum([x2 - x1 for x1, x2 in merged_ranges])


def part2(input):
    sensors = parse_input(input)
    # bound = 20
    bound = 4000000
    ranges = []
    for y_cutoff in range(bound + 1):
        if y_cutoff % 100000 == 0:
            print(f'{100.0 * y_cutoff / bound}%')
        cant_contain = list()
        for sx, sy, bx, by in sensors:
            # print(f'Sensor at ({sx}, {sy}) with beacon at ({bx}, {by})')
            d_sb = abs(sx - bx) + abs(sy - by)
            d_sl = abs(sy - y_cutoff)
            diff = d_sb - d_sl
            if diff >= 0:
                cant_contain.append([max(sx - diff, 0), min(sx + diff, bound)])
        cant_contain.sort()
        merged_ranges = [cant_contain[0]]
        for i in range(1, len(cant_contain)):
            if cant_contain[i][0] > merged_ranges[-1][1] + 1:
                merged_ranges.append(cant_contain[i])
            else:
                merged_ranges[-1][1] = max(cant_contain[i][1], merged_ranges[-1][1])
        ranges.append(merged_ranges)
    for y, rang in enumerate(ranges):
        if rang != [[0, bound]]:
            x = rang[0][1] + 1
            return y + x * 4000000


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
