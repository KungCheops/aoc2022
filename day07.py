from helper.input import read_input_simple
import sys
from collections import defaultdict
from queue import Queue


sizes_cache = dict()


def folder_size(folder, folder_structure):
    if folder in sizes_cache:
        return sizes_cache[folder]
    size = 0
    for a, b in folder_structure[folder]:
        if a == 'dir':
            size += folder_size(b, folder_structure)
        else:
            size += b
    sizes_cache[folder] = size
    return size


def folder_to_str(folder):
    return '/'.join(folder)


def create_structure(input):
    current_folder = []
    folder_structure = defaultdict(list)
    all_folders = {''}
    for line in read_input_simple(7, input):
        split_line = line.split()
        if split_line[0] == '$':
            if split_line[1] == 'cd':
                if split_line[2] == '..':
                    current_folder = current_folder[:-1]
                elif split_line[2] == '/':
                    current_folder = ['']
                else:
                    current_folder.append(split_line[2])
        else:
            new_folder = current_folder + [split_line[1]]
            if split_line[0] == 'dir':
                folder_structure[folder_to_str(current_folder)].append(('dir', folder_to_str(new_folder)))
                all_folders.add(folder_to_str(new_folder))
            else:
                folder_structure[folder_to_str(current_folder)].append((folder_to_str(new_folder), int(split_line[0])))
    return folder_structure, all_folders


def part1(input):
    folder_structure, all_folders = create_structure(input)
    small_folders_sum = 0
    for folder in all_folders:
        this_folder_size = folder_size(folder, folder_structure)
        if this_folder_size <= 100000:
            small_folders_sum += this_folder_size
    return small_folders_sum


def part2(input):
    folder_structure, all_folders = create_structure(input)
    disk_size = 70000000
    needed_free_space = 30000000
    total_used_size = folder_size('', folder_structure)
    need_to_remove = needed_free_space - disk_size + total_used_size
    smallest_large_folder_size = total_used_size
    for folder in all_folders:
        this_folder_size = folder_size(folder, folder_structure)
        if this_folder_size >= need_to_remove and this_folder_size < smallest_large_folder_size:
            smallest_large_folder_size = this_folder_size
    return smallest_large_folder_size


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
