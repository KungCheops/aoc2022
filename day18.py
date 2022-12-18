from helper.input import read_input
import sys
from collections import defaultdict
from queue import Queue


def is_neighbor(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2) == 1


def get_neighbors(p1):
    x1, y1, z1 = p1
    return {(x1,y1,z1+1),(x1,y1,z1-1),(x1,y1+1,z1),(x1,y1-1,z1),(x1+1,y1,z1),(x1-1,y1,z1)}


def can_reach(start, end, unreachable):
    to_visit = Queue()
    to_visit.put((start, []))
    visited = set()
    visited.add(start)

    while not to_visit.empty():
        current, path = to_visit.get()
        if current == end or current in end:
            return True

        neighbors = get_neighbors(current) - unreachable
        for neighbor in neighbors:
            if not neighbor in visited:
                to_visit.put((neighbor, path + [current]))
                visited.add(neighbor)
    return False


def part1(input):
    neighbors = defaultdict(int)

    for [x, y, z] in read_input(18, input, [(int,)]):
        p1 = (x, y, z)
        neighbors[p1] = 0
        for p2 in neighbors:
            if is_neighbor(p1, p2):
                neighbors[p1] += 1
                neighbors[p2] += 1

    return len(neighbors) * 6 - sum(neighbors.values())


def part2(input):
    sides = 0
    neighbors = defaultdict(set)
    cubes = set()
    minX = maxX = minY = maxY = minZ = maxZ = None

    for [x, y, z] in read_input(18, input, [(int,)]):
        if minX == None:
            minX = maxX = x
            minY = maxY = y
            minZ = maxZ = z
        else:
            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y
            if z < minZ:
                minZ = z
            if z > maxZ:
                maxZ = z
        p1 = (x, y, z)
        neighbors[p1] = set()
        cubes.add(p1)
        for p2 in neighbors:
            if is_neighbor(p1, p2):
                neighbors[p1].add(p2)
                neighbors[p2].add(p1)

    for z in range(minZ + 1, maxZ):
        for y in range(minY + 1, maxY):
            for x in range(minX + 1, maxX):
                p1 = (x, y, z)
                if not p1 in cubes:
                    distance_to_yz_plane = min(x - minX, maxX - x)
                    distance_to_zx_plane = min(y - minY, maxY - y)
                    distance_to_xy_plane = min(z - minZ, maxZ - z)
                    if distance_to_yz_plane <= distance_to_zx_plane and distance_to_yz_plane <= distance_to_xy_plane:
                        nearest_x = minX - 1 if x - minX < maxX - x else maxX + 1
                        p2 = (nearest_x, y, z)
                    elif distance_to_zx_plane <= distance_to_xy_plane:
                        nearest_y = minY - 1 if y - minY < maxY - y else maxY + 1
                        p2 = (x, nearest_y, z)
                    else:
                        nearest_z = minZ - 1 if z - minZ < maxZ - z else maxZ + 1
                        p2 = (x, y, nearest_z)
                    print(p1, p2)
                    if not can_reach(p1, p2, neighbors.keys()):
                        neighbors[p1] = set()
                        cubes.add(p1)
                        for p2 in neighbors:
                            if is_neighbor(p1, p2):
                                neighbors[p1].add(p2)
                                neighbors[p2].add(p1)

    return len(cubes) * 6 - sum((len(neighbor) for neighbor in neighbors.values()))


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
