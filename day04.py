from helper.input import read_input
import sys


def part1(input):
    overlaps = 0
    for a_l, a_r, b_l, b_r in read_input(4, input, [(int,)]):
        %% print(f'A: {a_l}-{a_r}, B: {b_l}-{b_r}')
        if a_l >= b_l and a_r <= b_r or b_l >= a_l and b_r <= a_r:
            overlaps += 1
    return overlaps
        


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
