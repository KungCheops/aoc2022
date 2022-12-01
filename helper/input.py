import re


def read_input(day, part):
    read_input(day, part, [str])


def read_input(day, part, fun_and_args):
    with open(f'input/day{day:02d}_{part}.txt') as file:
        for line in file:
            typed_split_line = []
            for sub_line in line.split('|'):
                split_line = re.findall(r"[\w']+", sub_line)
                extended_fun_and_args = fun_and_args
                while len(split_line) > len(extended_fun_and_args):
                    extended_fun_and_args += fun_and_args

                typed_split_line.append([fun(item, *args) for item, (fun, *args) in zip(split_line, fun_and_args)])
            if len(typed_split_line) == 1:
                yield typed_split_line[0]
            else:
                yield typed_split_line


def read_input_simple(day, part):
    with open(f'input/day{day:02d}_{part}.txt') as file:
        for line in file:
            yield line.strip()
