from helper.input import read_input
import sys


def part1(input):
    elf_load = 0
    max_elf_load = 0

    for value in read_input(1, input, [(int,)]):
        if not value:
            if elf_load > max_elf_load:
                max_elf_load = elf_load
            elf_load = 0
        else:
            item_weight = value[0]
            elf_load += item_weight
    return max_elf_load
            


def part2(input):
    elf_load = 0
    max_elf_load = [0, 0, 0]

    for value in read_input(1, input, [(int,)]):
        if not value:
            if elf_load > max_elf_load[0]:
                max_elf_load[2] = max_elf_load[1]
                max_elf_load[1] = max_elf_load[0]
                max_elf_load[0] = elf_load
            elif elf_load > max_elf_load[1]:
                max_elf_load[2] = max_elf_load[1]
                max_elf_load[1] = elf_load
            elif elf_load > max_elf_load[2]:
                max_elf_load[2] = elf_load
            elf_load = 0
        else:
            item_weight = value[0]
            elf_load += item_weight
    return sum(max_elf_load), max_elf_load


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
