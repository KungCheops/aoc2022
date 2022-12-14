from helper.input import read_input_simple
import sys


sand_spawn = (500, 0)


def draw_map(rock, sand, bounds):
    for y in range(bounds[2], bounds[3]):
        print(''.join(('+' if (x, y) == (sand_spawn[0], sand_spawn[1]) else '#' if (x, y) in rock else 'o' if (x, y) in sand else ' ') for x in range(bounds[0], bounds[1])))
    print()


def update_bounds(x, y, bounds):    
    if x < bounds[0]:
        bounds[0] = x
    if x >= bounds[1]:
        bounds[1] = x + 1
    if y < bounds[2]:
        bounds[2] = y
    if y >= bounds[3]:
        bounds[3] = y + 1


def create_map(input):
    rock = set()
    bounds = [sand_spawn[0], sand_spawn[0] + 1, sand_spawn[1], sand_spawn[1] + 1]
    for line in read_input_simple(14, input):
        x2, y2 = None, None
        for x1, y1 in (map(int, (coordinate.split(','))) for coordinate in line.split(' -> ')):
            update_bounds(x1, y1, bounds)
            if x2 and y2:
                if x1 == x2:
                    sy = min(y1, y2)
                    ty = max(y1, y2) + 1
                    for y in range(sy, ty):
                        rock.add((x1, y))
                elif y1 == y2:
                    sx = min(x1, x2)
                    tx = max(x1, x2) + 1
                    for x in range(sx, tx):
                        rock.add((x, y1))
            x2, y2 = x1, y1
    return rock, bounds


def at_rest(x, y, rock_sand):
    return (x, y + 1) in rock_sand and (x - 1, y + 1) in rock_sand and (x + 1, y + 1) in rock_sand


def get_next_position(x, y, rock_sand):
    if not (x, y + 1) in rock_sand:
        return x, y + 1
    elif not (x - 1, y + 1) in rock_sand:
        return x - 1, y + 1
    elif not (x + 1, y + 1) in rock_sand:
        return x + 1, y + 1
    else:
        return


def drop_sand(rock, bounds):
    sand = set()
    rock_sand = rock.union(sand)
    draw_map(rock, sand, bounds)
    grains = 0

    updated = True
    while updated:
        grain_x, grain_y = sand_spawn
        while not at_rest(grain_x, grain_y, rock_sand):
            grain_x, grain_y = get_next_position(grain_x, grain_y, rock_sand)
            if grain_y > bounds[3]:
                updated = False
                break
        if updated:
            sand.add((grain_x, grain_y))
            rock_sand.add((grain_x, grain_y))
            grains += 1
            if grains % 100 == 0:
                draw_map(rock, sand, bounds)
                print(grains)
            update_bounds(grain_x, grain_y, bounds)
            if (grain_x, grain_y) == sand_spawn:
                break

    draw_map(rock, sand, bounds)
    return grains


def part1(input):
    rock, bounds = create_map(input)
    return drop_sand(rock, bounds)


def part2(input):
    rock, bounds = create_map(input)
    for x in range(0, 1000):
        rock.add((x, bounds[3] + 1))
    bounds[3] += 2
    return drop_sand(rock, bounds)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
