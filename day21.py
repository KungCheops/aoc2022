from helper.input import read_input_simple
import sys
import operator


def get_operator(op_str):
    match op_str:
        case '+':
            return operator.add
        case '-':
            return operator.sub
        case '*':
            return operator.mul
        case '/':
            return operator.floordiv


def parse_input(input):
    monkeys = dict()
    for line in read_input_simple(21, input):
        split_line = line.replace(':', '').split()
        if len(split_line) == 2:
            monkeys[split_line[0]] = int(split_line[1])
        elif len(split_line) == 4:
            monkeys[split_line[0]] = (get_operator(split_line[2]), split_line[1], split_line[3])
    return monkeys


def evaluate(monkey, monkeys):
    val = monkeys[monkey]
    if isinstance(val, int):
        return val
    else:
        op, m1, m2 = val
        return op(evaluate(m1, monkeys), evaluate(m2, monkeys))


def part1(input):
    monkeys = parse_input(input)
    
    root_value = evaluate('root', monkeys)
    
    return root_value


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
