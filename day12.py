from helper.input import read_input_simple
import sys
import numpy as np
from queue import Queue


def create_map(input):
    height_map = []
    start = None
    end = None
    for y, line in enumerate(read_input_simple(12, input)):
        new_line = []
        for x, char in enumerate(line):
            if char == 'S':
                start = (x, y)
                new_line.append(0) # 'a' 
            elif char == 'E':
                end = (x, y)
                new_line.append(25) # 'z'
            else:
                new_line.append(ord(char) - 97) # ord('a')
        height_map.append(new_line)
    return np.array(height_map), start, end


def neighboring_cells(cell, height_map):
    x, y = cell
    neighbors = []
    for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if y1 >= 0 and y1 < len(height_map) and x1 >= 0 and x1 < len(height_map[y1]):
            if (height_map[y1][x1] - height_map[y][x]) <= 1:
                neighbors.append((x1, y1))
            # else:
                # print(f'Couldn\'t go from {(x, y)} to {(x1, y1)} ({height_map[y][x]} to {height_map[y1][x1]})')
    return neighbors


def dijkstra(height_map, start, end):
    to_visit = Queue()
    to_visit.put((start, []))
    visited = set()
    visited.add(start)
    
    while not to_visit.empty():
        current, path = to_visit.get()
        # print(len(visited), to_visit.qsize(), len(path), current)
        if current == end:
            return path + [current]
        
        for neighbor in neighboring_cells(current, height_map):
            if not neighbor in visited:
                to_visit.put((neighbor, path + [current]))
                visited.add(neighbor)

    return
        


def part1(input):
    height_map, start, end = create_map(input)
    path = dijkstra(height_map, start, end)
    return len(path) - 1


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
