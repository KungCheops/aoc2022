from helper.input import read_input
import sys


def find_marker(string, size):
    last_four = [None] * (size + 1)
    index = 0
    for char in string:
        if len(set(last_four)) == len(last_four):
            break
        last_four[index%size] = char
        index += 1
    return index


def part1(input):
    markers = []
    for [line] in read_input(6, input, [(str,)]):
        markers.append(find_marker(line, 4))
    return markers


def part2(input):
    markers = []
    for [line] in read_input(6, input, [(str,)]):
        markers.append(find_marker(line, 14))
    return markers


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
