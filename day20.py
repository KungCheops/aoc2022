from helper.input import read_input_simple
import sys


def input_to_gen(input):
    for line in read_input_simple(20, input):
        yield(int(line))


def move(index, lst, indices):
    new_index = index + lst[index]
    while new_index >= len(lst):
        new_index = new_index % len(lst) + new_index // len(lst)
    while new_index < 0:
        new_index = new_index % len(lst) + new_index // len(lst)
    if new_index == 0:
        if index == 0:
            return lst, indices
        else:
            new_lst = lst[:index] + lst[index+1:] + [lst[index]]
            new_indices = [i - 1 if i > index else len(lst) - 1 if i == index else i for i in indices]
            return new_lst, new_indices
    if new_index > index:
        new_lst = lst[:index] + lst[index+1:new_index+1] + [lst[index]] + lst[new_index+1:]
        new_indices = [i - 1 if i > index and i <= new_index else new_index if i == index else i for i in indices]
        return new_lst, new_indices
    elif new_index < index:
        new_lst = lst[:new_index] + [lst[index]] + lst[new_index:index] + lst[index+1:]
        new_indices = [i + 1 if i >= new_index and i < index else new_index if i == index else i for i in indices]
        return new_lst, new_indices
    else:
        return lst[:], indices[:]


def mix(lst, times=1):
    indices = list(range(0, len(lst)))

    for _ in range(times):
        for i in range(len(lst)):
            to_swap_index = indices[i]
            lst, indices = move(to_swap_index, lst, indices)

    return lst


def part1(input):
    encrypted = list(input_to_gen(input))
    decrypted = mix(encrypted)
    index_of_zero = decrypted.index(0)
    items = [decrypted[(index_of_zero + i * 1000) % len(decrypted)] for i in range(1,4)]
    return sum(items)


def part2(input):
    encrypted = list(input_to_gen(input))
    decrypted = [i * 811589153 for i in encrypted]

    decrypted = mix(decrypted, 10)
    index_of_zero = decrypted.index(0)
    items = [decrypted[(index_of_zero + i * 1000) % len(decrypted)] for i in range(1,4)]
    return sum(items)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
