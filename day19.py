from helper.input import read_input_simple
import sys
import functools
import itertools
import math


def parse_input(input):
    for line in read_input_simple(19, input):
        bid, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = (int(token) for token in line.replace(':', '').split(' ') if token.isdigit())
        yield (bid, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)


# @functools.lru_cache(maxsize=None)
def optimal_solution(time_remaining, robots, resources, max_robots, blueprint):
    # print(time_remaining, robots, resources)
    ore, clay, obsidian, geodes = resources
    ore_robots, clay_robots, obs_robots, geo_robots = robots
    max_ore_robots, max_clay_robots, max_obs_robots = max_robots
    ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = blueprint

    value = time_remaining * geo_robots
    path = [(time_remaining, robots, resources)]

    # Build geode robot
    if ore_robots > 0 and obs_robots > 0:
        time_until_next = max(max(math.ceil((geo_ore - ore) / ore_robots), math.ceil((geo_obs - obsidian) / obs_robots)) + 1, 1)
        if time_until_next < time_remaining:
            new_robots = (ore_robots, clay_robots, obs_robots, geo_robots + 1)
            new_ore = ore - geo_ore
            new_obs = obsidian - geo_obs
            new_resources = (new_ore, clay, new_obs, geodes)
            new_resources = tuple(resource + robot * time_until_next for resource, robot in zip(new_resources, robots))
            new_value, new_path = optimal_solution(time_remaining - time_until_next, new_robots, new_resources, max_robots, blueprint)
            new_value += geo_robots * time_until_next
            if new_value > value:
                value = new_value
                path = new_path + [(time_remaining, robots, resources)]

    # Build obsidian robot
    if ore_robots > 0 and clay_robots > 0 and obs_robots < max_obs_robots:
        time_until_next = max(max(math.ceil((obs_ore - ore) / ore_robots), math.ceil((obs_clay - clay) / clay_robots)) + 1, 1)
        if time_until_next < time_remaining:
            new_robots = (ore_robots, clay_robots, obs_robots + 1, geo_robots)
            new_ore = ore - obs_ore
            new_clay = clay - obs_clay
            new_resources = (new_ore, new_clay, obsidian, geodes)
            new_resources = tuple(resource + robot * time_until_next for resource, robot in zip(new_resources, robots))
            new_value, new_path = optimal_solution(time_remaining - time_until_next, new_robots, new_resources, max_robots, blueprint)
            new_value += geo_robots * time_until_next
            if new_value > value:
                value = new_value
                path = new_path + [(time_remaining, robots, resources)]

    # Build clay robot
    if ore_robots > 0 and clay_robots < max_clay_robots:
        time_until_next = max(math.ceil((clay_ore - ore) / ore_robots) + 1, 1)
        if time_until_next < time_remaining:
            new_robots = (ore_robots, clay_robots + 1, obs_robots, geo_robots)
            new_ore = ore - clay_ore
            new_resources = (new_ore, clay, obsidian, geodes)
            new_resources = tuple(resource + robot * time_until_next for resource, robot in zip(new_resources, robots))
            new_value, new_path = optimal_solution(time_remaining - time_until_next, new_robots, new_resources, max_robots, blueprint)
            new_value += geo_robots * time_until_next
            if new_value > value:
                value = new_value
                path = new_path + [(time_remaining, robots, resources)]

    # Build ore robot
    if ore_robots > 0 and ore_robots < max_ore_robots:
        time_until_next = max(math.ceil((ore_ore - ore) / ore_robots) + 1, 1)
        if time_until_next < time_remaining:
            new_robots = (ore_robots + 1, clay_robots, obs_robots, geo_robots)
            new_ore = ore - ore_ore
            new_resources = (new_ore, clay, obsidian, geodes)
            new_resources = tuple(resource + robot * time_until_next for resource, robot in zip(new_resources, robots))
            new_value, new_path = optimal_solution(time_remaining - time_until_next, new_robots, new_resources, max_robots, blueprint)
            new_value += geo_robots * time_until_next
            if new_value > value:
                value = new_value
                path = new_path + [(time_remaining, robots, resources)]

    return value, path


def part1(input):
    blueprints = parse_input(input)
    ret = 0
    
    for blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs in blueprints:
        # print(blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)
        max_ore_robots = max(ore_ore, clay_ore, obs_ore, geo_ore)
        max_clay_robots = obs_clay
        max_obs_robots = geo_obs
        value, path = optimal_solution(24, (1, 0, 0, 0), (0, 0, 0, 0), (max_ore_robots, max_clay_robots, max_obs_robots), (ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs))
        print(blueprint_id, value)
        # [print(step) for step in reversed(path)]
        ret += value * blueprint_id
    
    return ret


def part2(input):
    blueprints = parse_input(input)
    ret = 0
    
    for blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs in itertools.islice(blueprints, 3):
        # print(blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)
        max_ore_robots = max(ore_ore, clay_ore, obs_ore, geo_ore)
        max_clay_robots = obs_clay
        max_obs_robots = geo_obs
        value, path = optimal_solution(32, (1, 0, 0, 0), (0, 0, 0, 0), (max_ore_robots, max_clay_robots, max_obs_robots), (ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs))
        print(blueprint_id, value)
        # [print(step) for step in reverse(path)]
        ret += value * blueprint_id
    
    return ret


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
