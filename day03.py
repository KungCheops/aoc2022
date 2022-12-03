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
            a, b, c = lines
            largest = 'A'
            index_a = 0
            index_b = 0
            index_c = 0
            value_a = a[index_a]
            if value_a > largest:
                largest = value_a
            value_b = b[index_b]
            if value_b > largest:
                largest = value_b
            value_c = c[index_c]
            if value_c > largest:
                largest = value_c
            while index_a < len(a) and index_b < len(b) and index_c < len(c):
                if value_a == value_b and value_a == value_c:
                    break
                else:
                    if value_a < largest:
                        index_a += 1
                        value_a = a[index_a]
                        if value_a > largest:
                            largest = value_a
                    if value_b < largest:
                        index_b += 1
                        value_b = b[index_b]
                        if value_b > largest:
                            largest = value_b
                    if value_c < largest:
                        index_c += 1
                        value_c = c[index_c]
                        if value_c > largest:
                            largest = value_c
            total += priority(value_a)
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
