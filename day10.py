from helper.input import read_input_simple
import sys
from itertools import starmap
import numpy as np
import matplotlib.pyplot as plt


def part1(input):
    cycle = 0
    total = 0
    register_x = 1
    break_points = [20 + 40 * i for i in range(6)]
    current_point = 0
    levels = []
    for command in read_input_simple(10, input):
        command = command.split()
        if command[0] == 'noop':
            cycle += 1
            if cycle >= break_points[current_point]:
                levels.append(register_x)
                current_point += 1
                if current_point >= len(break_points):
                    break
        if command[0] == 'addx':
            cycle += 2
            if cycle >= break_points[current_point]:
                levels.append(register_x)
                current_point += 1
                if current_point >= len(break_points):
                    break
            register_x += int(command[1])
    return levels, sum(starmap(lambda a, b: a * b, zip(levels, break_points)))


def update_image(image, cycle, register_x):
    x_pos = cycle % 40
    pixel = 0
    if abs(x_pos - register_x) <= 1:
        pixel = 1
    y_pos = cycle // 40
    if y_pos >= len(image):
        image.append([0] * 40)
    image[y_pos][x_pos] = pixel
    return image


def image_to_string(image):
    return '\n'.join(''.join('#' if pixel == 1 else '.' for pixel in row) for row in image)


def part2(input):
    image = [[0] * 40]
    register_x = 1
    cycle = 0
    for command in read_input_simple(10, input):
        command = command.split()
        image = update_image(image, cycle, register_x)
        if command[0] == 'noop':
            cycle += 1
        if command[0] == 'addx':
            cycle += 1
            image = update_image(image, cycle, register_x)
            cycle += 1
            register_x += int(command[1])
    # plt.imshow(np.array(image), interpolation='nearest')
    # plt.show()
    return image_to_string(image)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
