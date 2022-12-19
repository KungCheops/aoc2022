from helper.input import read_input_simple
import sys
import functools
import itertools


def parse_input(input):
    for line in read_input_simple(19, input):
        bid, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = (int(token) for token in line.replace(':', '').split(' ') if token.isdigit())
        yield (bid, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)


@functools.lru_cache(maxsize=None)
def optimal_solution(time_remaining, robots, resources, blueprint):
    ore, clay, obsidian, geodes = resources
    if time_remaining == 0:
        return geodes
    ore_robots, clay_robots, obs_robots, geo_robots = robots
    ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs = blueprint
    
    new_ore, new_clay, new_obs, new_geo = ore + ore_robots, clay + clay_robots, obsidian + obs_robots, geodes + geo_robots
    new_resources = (new_ore, new_clay, new_obs, new_geo)
    value = geodes
    
    if geo_ore <= ore and geo_obs <= obsidian:
        new_robots = (ore_robots, clay_robots, obs_robots, geo_robots + 1)
        new_resources_geo = (new_ore - geo_ore, new_clay, new_obs - geo_obs, new_geo)
        return optimal_solution(time_remaining - 1, new_robots, new_resources_geo, blueprint)
    else:
        if obs_ore <= ore and obs_clay <= clay:
            new_robots = (ore_robots, clay_robots, obs_robots + 1, geo_robots)
            new_resources_obs = (new_ore - obs_ore, new_clay - obs_clay, new_obs, new_geo)
            new_value = optimal_solution(time_remaining - 1, new_robots, new_resources_obs, blueprint)
            if new_value > value:
                value = new_value
        if obs_ore > ore or obs_clay > clay or ore - obs_ore <= geo_ore + 1:
            if ore_ore <= ore:
                new_robots = (ore_robots + 1, clay_robots, obs_robots, geo_robots)
                new_resources_ore = (new_ore - ore_ore, new_clay, new_obs, new_geo)
                new_value = optimal_solution(time_remaining - 1, new_robots, new_resources_ore, blueprint)
                if new_value > value:
                    value = new_value
            if clay_ore <= ore:
                new_robots = (ore_robots, clay_robots + 1, obs_robots, geo_robots)
                new_resources_clay = (new_ore - clay_ore, new_clay, new_obs, new_geo)
                new_value = optimal_solution(time_remaining - 1, new_robots, new_resources_clay, blueprint)
                if new_value > value:
                    value = new_value
            if ore_ore > ore or clay_ore > ore:
                new_value = optimal_solution(time_remaining - 1, robots, new_resources, blueprint)
                if new_value > value:
                    value = new_value
    return value


def optimal_solution2(time_remaining, robots, resources, blueprint):
    pass


def part1(input):
    blueprints = parse_input(input)
    ret = 0
    
    for blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs in blueprints:
        print(blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)
        value = optimal_solution(24, (1, 0, 0, 0), (0, 0, 0, 0), (ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs))
        print(value)
        ret += value * blueprint_id
    
    return ret


def part2(input):
    blueprints = parse_input(input)
    ret = 0
    
    for blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs in itertools.islice(blueprints, 3):
        print(blueprint_id, ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs)
        ore, clay, obsidian, geodes = optimal_solution(32, (1, 0, 0, 0), (0, 0, 0, 0), (ore_ore, clay_ore, obs_ore, obs_clay, geo_ore, geo_obs))
        print(blueprint_id, ore, clay, obsidian, geodes)
        ret += geodes * blueprint_id
    
    return ret


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
