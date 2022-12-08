from helper.input import read_input_simple
import numpy as np
import sys
import matplotlib.pyplot as plt


def create_map(input):
    tree_map = []
    for line in read_input_simple(8, input):
        tree_map.append(list(int(char) for char in line))
    return np.array(tree_map)


def part1(input):
    tree_map = create_map(input)
    visibility_map = np.zeros(tree_map.shape)
    
    # west to east
    for y in range(0, len(tree_map)):
        max_seen = -1
        for x in range(0, len(tree_map[y])):
            if tree_map[y][x] > max_seen:
                visibility_map[y][x] = 1
                max_seen = tree_map[y][x]
    
    # east to west
    for y in range(0, len(tree_map)):
        max_seen = -1
        for x in reversed(range(0, len(tree_map[y]))):
            if tree_map[y][x] > max_seen:
                visibility_map[y][x] = 1
                max_seen = tree_map[y][x]
    
    # north to south
    for y in range(0, len(tree_map.T)):
        max_seen = -1
        for x in range(0, len(tree_map.T[y])):
            if tree_map.T[y][x] > max_seen:
                visibility_map[x][y] = 1
                max_seen = tree_map.T[y][x]
    
    # east to west
    for y in range(0, len(tree_map.T)):
        max_seen = -1
        for x in reversed(range(0, len(tree_map.T[y]))):
            if tree_map.T[y][x] > max_seen:
                visibility_map[x][y] = 1
                max_seen = tree_map.T[y][x]

    plt.subplot(1,2,1)
    plt.imshow(tree_map, interpolation='nearest')
    plt.subplot(1,2,2)
    plt.imshow(visibility_map, interpolation='nearest')
    plt.show()
    return int(np.sum(visibility_map))


def part2(input):
    tree_map = create_map(input)
    scenery_map = np.zeros(tree_map.shape)
    
    for sy in range(len(tree_map)):
        for sx in range(len(tree_map[sy])):
            scenery_score = 1
            my_height = tree_map[sy][sx]
            
            # west to east
            num_seen = 0
            for x in range(sx + 1, len(tree_map[sy])):
                if tree_map[sy][x] < my_height:
                    num_seen += 1
                else:
                    num_seen += 1
                    break
            scenery_score *= num_seen
            
            # east to west
            num_seen = 0
            for x in range(sx - 1, -1, -1):
                if tree_map[sy][x] < my_height:
                    num_seen += 1
                else:
                    num_seen += 1
                    break
            scenery_score *= num_seen
            
            # north to south
            num_seen = 0
            for y in range(sy + 1, len(tree_map)):
                if tree_map[y][sx] < my_height:
                    num_seen += 1
                else:
                    num_seen += 1
                    break
            scenery_score *= num_seen
            
            # south to north
            num_seen = 0
            for y in range(sy - 1, -1, -1):
                if tree_map[y][sx] < my_height:
                    num_seen += 1
                else:
                    num_seen += 1
                    break
            scenery_score *= num_seen
            
            scenery_map[sy][sx] = scenery_score
    plt.subplot(1,2,1)
    plt.imshow(tree_map, interpolation='nearest')
    plt.subplot(1,2,2)
    plt.imshow(scenery_map, interpolation='nearest')
    plt.show()
    return int(np.max(scenery_map))

if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
