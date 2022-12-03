from helper.input import read_input
import sys


def priority(x):
    if x.isupper():
        return ord(x) - ord('A') + 27
    elif x.islower():
        return ord(x) - ord('a') + 1


def part1(input):
    total = 0
    for [line] in read_input(3, input, [(str,)]):
        a, b = sorted(line[:len(line)//2]), sorted(line[len(line)//2:])
        index_a = 0
        index_b = 0
        value_a = a[index_a]
        value_b = b[index_b]
        while index_a < len(a) and index_b < len(b):
            if value_a == value_b:
                break
            elif value_a < value_b:
                index_a += 1
                value_a = a[index_a]
            else:
                index_b += 1
                value_b = b[index_b]
        total += priority(value_a)
    return total
            


def part2(input):
    total = 0
    lines = []
    for [line] in read_input(3, input, [(str,)]):
        lines.append(sorted(line))
        if len(lines) == 3:
            largest = 'A'
            indices = [0] * 3
            values = [0] * 3

            for i in range(3):
                values[i] = lines[i][indices[i]]
                if lines[i][indices[i]] > largest:
                    largest = lines[i][indices[i]]

            while all([index < len(line) for index, line in zip(indices, lines)]):
                if all(value == values[0] for value in values[1:]):
                    break
                else:
                    for i in range(3):
                        if values[i] < largest:
                            indices[i] += 1
                            values[i] = lines[i][indices[i]]
                            if values[i] > largest:
                                largest = values[i]

            total += priority(values[0])
            lines = []
    return total


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
