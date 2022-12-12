from helper.input import read_input_simple
import sys
import numpy as np
from queue import Queue
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec


def create_map(input, all_starts = False):
    height_map = []
    start = None
    all_starts = set()
    end = None
    for y, line in enumerate(read_input_simple(12, input)):
        new_line = []
        for x, char in enumerate(line):
            if char == 'S':
                start = (x, y)
                all_starts.add((x, y))
                new_line.append(0) # 'a' 
            elif char == 'E':
                end = (x, y)
                new_line.append(25) # 'z'
            else:
                new_line.append(ord(char) - 97) # ord('a')
                if char == 'a':
                    all_starts.add((x, y))
        height_map.append(new_line)
    return np.array(height_map), start, end, all_starts


def neighboring_cells(cell, height_map):
    x, y = cell
    neighbors = []
    for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if y1 >= 0 and y1 < len(height_map) and x1 >= 0 and x1 < len(height_map[y1]):
            if height_map[y][x] - height_map[y1][x1] <= 1:
                neighbors.append((x1, y1))
    return neighbors


def dijkstra(height_map, start, end):
    to_visit = Queue()
    to_visit.put((start, []))
    visited = set()
    visited.add(start)
    
    while not to_visit.empty():
        current, path = to_visit.get()
        if current == end or current in end:
            return list(reversed(path + [current]))
        
        for neighbor in neighboring_cells(current, height_map):
            if not neighbor in visited:
                to_visit.put((neighbor, path + [current]))
                visited.add(neighbor)
    return


def path_to_map(path, height_map):
    new_map = height_map.copy()
    path_len = len(path)
    counter = 1
    for x, y in path:
        new_map[y][x] = 40 + ((10 * counter) // path_len)
        counter += 1
    return new_map


def plot_map(height_map, axis):
    axis.imshow(height_map, interpolation='nearest')

def plot_path(height_map, path, axis):
    axis.imshow(path_to_map(path, height_map), interpolation='nearest')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: py day12.py <input file (without extension)>')
    _, input = sys.argv
    height_map, start, end, all_starts = create_map(input)
    path1 = dijkstra(height_map, end, start)
    path2 = dijkstra(height_map, end, all_starts)
    fig = plt.figure()
    gs = GridSpec(2, 2, figure=fig)
    ax1 = fig.add_subplot(gs[:, 0])
    ax1.set_title('Map')
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title(f'Path 1 (length: {len(path1) - 1})')
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_title(f'Path 2 (length: {len(path2) - 1})')
    plot_map(height_map, ax1)
    plot_path(height_map, path1, ax2)
    plot_path(height_map, path2, ax3)
    plt.show()
