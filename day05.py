from helper.input import read_input_simple
import sys


def parse_input(lines):
    num_buckets = len(lines[0]) // 4 + 1
    bucket = [[] for _ in range(num_buckets)]
    line_index = 0
    line = lines[line_index]
    while line:
        for i in range(1, len(line), 4):
            if line[i].isalpha():
                bucket[(i-1)//4].append(line[i])
        line_index += 1
        line = lines[line_index]
    instructions = []
    for line in lines[line_index + 1:]:
        instructions.append([int(d) for d in line.split() if d.isdigit()])
    return bucket, instructions

def part1(input):
    bucket, instructions = parse_input(list(read_input_simple(5, input, False)))
    for amount, source, target in instructions:
        bucket[target - 1] = list(reversed(bucket[source - 1][:amount])) + bucket[target - 1]
        bucket[source - 1] = bucket[source - 1][amount:]
    return ''.join([b[0] for b in bucket])


def part2(input):
    bucket, instructions = parse_input(list(read_input_simple(5, input, False)))
    for amount, source, target in instructions:
        bucket[target - 1] = bucket[source - 1][:amount] + bucket[target - 1]
        bucket[source - 1] = bucket[source - 1][amount:]
    return ''.join([b[0] for b in bucket])


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
