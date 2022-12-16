from helper.input import read_input_simple
import sys
from queue import Queue
import itertools


def get_distance(start, end, graph):
    # print(f'Distance from {start} to {end} in {graph}')
    to_visit = Queue()
    to_visit.put((start, []))
    visited = set()
    visited.add(start)
    
    while not to_visit.empty():
        current, path = to_visit.get()
        if current == end or current in end:
            # print(f'\tis {len(path)}')
            return len(path) + 1
        
        for neighbor in graph[current]:
            if not neighbor in visited:
                to_visit.put((neighbor, path + [current]))
                visited.add(neighbor)
    return None


def parse_input(input):
    valves = list()
    leads_to = dict()
    flow_rate = dict()
    
    for line in read_input_simple(16, input):
        _, valve, _, _, rate, _, _, _, _, *leads_to_valves = line.split()
        leads_to[valve] = [valve2.replace(',', '') for valve2 in leads_to_valves]
        flow_rate[valve] = int(rate[5:-1])
        valves.append(valve)
    valves.sort()
    distance_between = dict()
    
    valves = ['AA'] + [valve for valve in valves if flow_rate[valve] > 0]
    
    for i in range(len(valves) - 1):
        for j in range(i + 1, len(valves)):
            distance = get_distance(valves[i], valves[j], leads_to)
            distance_between[(valves[i], valves[j])] = distance_between[(valves[j], valves[i])] = distance
    
    return valves, flow_rate, distance_between


def get_flow(valves, flow_rates, time):
    value = sum([flow_rate * time for valve, flow_rate in flow_rates.items() if valve in valves])
    # print('\t\tFlow for', valves, flow_rates, time, 'is', value)
    return value


memo = dict()
memo_used = [0, 0]


def get_best_path(current, remaining_valves, distances, flow_rates, remaining_time, open_valves = set()):
    if remaining_time == 0:
        # print(f'Ran out of time with {open_valves} open.')
        return 0, []
    elif not remaining_valves:
        value = get_flow(open_valves, flow_rates, remaining_time)
        # print(f'Staying at {current} for {remaining_time} minute(s) with all vents open yields {value}.')
        return value, []
    else:
        sorted_remaining = tuple(sorted(list(remaining_valves)))
        sorted_open = tuple(sorted(list(open_valves)))
        key = (current, sorted_remaining, sorted_open, remaining_time)
        if key in memo:
            memo_used[0] += 1
            return memo[key]
        else:
            memo_used[1] += 1
        max_value = 0
        max_value_path = []
        for new in remaining_valves:
            new_remaining = remaining_valves.copy()
            new_remaining.remove(new)
            new_open = open_valves.copy()
            new_open.add(new)
            distance = distances[(current, new)]
            new_remaining_time = max(remaining_time - distance, 0)
            # print(f'Try going from {current} to {new} ({distance} minute(s) away):')
            released_while_travelling = get_flow(open_valves, flow_rates, min(distance, remaining_time))
            released_in_next_steps, path = get_best_path(new, new_remaining, distances, flow_rates, new_remaining_time, new_open)
            value = released_while_travelling + released_in_next_steps
            # print(f'\tValue of going from {current} to {new} with {open_valves} open valves and {remaining_time} minute(s) remaining is {released_while_travelling}+{released_in_next_steps}={value}.')
            if value > max_value:
                max_value = value
                max_value_path = path + [(new, new_remaining_time)]
        memo[key] = (max_value, max_value_path)
        return memo[key]


def all_valve_combinations(valves):
    res_set = set()
    for l in range(7, len(valves) // 2 + 1):
        combis = set(itertools.combinations(valves,l))
        for c in combis:
            res_set.add((tuple(c), tuple(set(valves)-set(c))))
    return res_set


def part1(input):
    valves, flow_rate, distance_between = parse_input(input)
    best_path = get_best_path(valves[0], set(valves[1:]), distance_between, flow_rate, 30)
    print(memo_used)
    return best_path


def part2(input):
    valves, flow_rate, distance_between = parse_input(input)
    best_score = 0
    best_path = None
    all_combinations = all_valve_combinations(valves[1:])
    number_of_combinations = len(all_combinations)
    for i, (valves1, valves2) in enumerate(all_combinations):
        print(f'Finding value for {valves1}, {valves2}: (progress: {i+1}/{number_of_combinations})')
        best_path_len1, path1 = get_best_path('AA', set(valves1), distance_between, flow_rate, 26)
        best_path_len2, path2 = get_best_path('AA', set(valves2), distance_between, flow_rate, 26)
        value = best_path_len1 + best_path_len2
        print(f'\t{best_path_len1}+{best_path_len2}={value}')
        if value > best_score:
            best_score = value
            best_path = (path1, path2)
    print(memo_used)
    return best_score, best_path


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
