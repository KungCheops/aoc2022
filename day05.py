from helper.input import read_input_simple
import sys


def parse_input(lines):
    num_buckets = len(lines[0]) // 4 + 1
    buckets = [[] for _ in range(num_buckets)]
    line_index = 0
    line = lines[line_index]
    while line:
        for i in range(1, len(line), 4):
            if line[i].isalpha():
                buckets[(i-1)//4].append(line[i])
        line_index += 1
        line = lines[line_index]
    instructions = []
    for line in lines[line_index + 1:]:
        instructions.append([int(d) for d in line.split() if d.isdigit()])
    return buckets, instructions


def print_buckets(buckets):
    height = max(len(bucket) for bucket in buckets)
    for row in (range(height)):
        row_lines = []
        for col in range(len(buckets)):
            if len(buckets[col]) >= height - row:
                # print(f'[{col}, {row}]: ', end='')
                # print(buckets[col])
                row_lines.append(f'[{buckets[col][row-height+len(buckets[col])]}]')
            else:
                row_lines.append('   ')
        print(' '.join(row_lines))
    print(' '.join(f' {i + 1} ' for i in range(len(buckets))))
    print()


def part1(input):
    buckets, instructions = parse_input(list(read_input_simple(5, input, False)))
    print_buckets(buckets)
    for amount, source, target in instructions:
        buckets[target - 1] = list(reversed(buckets[source - 1][:amount])) + buckets[target - 1]
        buckets[source - 1] = buckets[source - 1][amount:]
        print_buckets(buckets)
    return ''.join([b[0] for b in buckets])


def part2(input):
    buckets, instructions = parse_input(list(read_input_simple(5, input, False)))
    print_buckets(buckets)
    for amount, source, target in instructions:
        buckets[target - 1] = buckets[source - 1][:amount] + buckets[target - 1]
        buckets[source - 1] = buckets[source - 1][amount:]
        print_buckets(buckets)
    return ''.join([b[0] for b in buckets])


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
