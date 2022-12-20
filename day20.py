from helper.input import read_input_simple
import sys


def input_to_gen(input):
    for line in read_input_simple(20, input):
        yield(int(line))


def move(index, lst, indices):
    new_index = index + lst[index]
    # print(f'Moving item {lst[index]} at index {index} to {new_index}')
    while new_index >= len(lst):
        new_index -= (len(lst) - 1)
    while new_index < 0:
        new_index += (len(lst) - 1)
    if new_index == 0:
        if index == 0:
            return lst, index_lst
        else:
            new_lst = lst[:index] + lst[index+1:] + [lst[index]]
            new_indices = [i - 1 if i > index else len(lst) - 1 if i == index else i for i in indices]
            return new_lst, new_indices
    # print(f'\tUpdated index: {new_index}')
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


def swap_items(lst):
    indices = list(range(0, len(lst)))
    print(lst)

    # print(move(0, [1, 2, -3, 3, -2, 0, 4]), [2, 1, -3, 3, -2, 0, 4])
    # print(move(0, [2, 1, -3, 3, -2, 0, 4]), [1, -3, 2, 3, -2, 0, 4])
    # print(move(1, [1, -3, 2, 3, -2, 0, 4]), [1, 2, 3, -2, -3, 0, 4])
    # print(move(2, [1, 2, 3, -2, -3, 0, 4]), [1, 2, -2, -3, 0, 3, 4])
    # print(move(2, [1, 2, -2, -3, 0, 3, 4]), [1, 2, -3, 0, 3, 4, -2])
    # print(move(3, [1, 2, -3, 0, 3, 4, -2]), [1, 2, -3, 0, 3, 4, -2])
    # print(move(5, [1, 2, -3, 0, 3, 4, -2]), [1, 2, -3, 4, 0, 3, -2])

    for i in range(len(lst)):
        to_swap_index = indices[i]
        lst, indices = move(to_swap_index, lst, indices)
    print(lst)

    index_of_zero = lst.index(0)
    return [lst[(index_of_zero + i * 1000) % len(lst)] for i in range(1,4)]


def part1(input):
    encrypted = list(input_to_gen(input))
    items = swap_items(encrypted)
    return sum(items)


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
