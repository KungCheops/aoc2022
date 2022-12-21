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
            monkeys[split_line[0]] = (split_line[2], split_line[1], split_line[3])
    return monkeys


def evaluate(monkey, monkeys):
    val = monkeys[monkey]
    if type(val) in {int, str}:
        return val
    elif isinstance(val, tuple):
        op_str, m1, m2 = val
        op = get_operator(op_str)
        v1 = evaluate(m1, monkeys)
        v2 = evaluate(m2, monkeys)
        if op_str == '=':
            return (v1, v2)
        if isinstance(v1, int) and isinstance(v2, int):
            return op(v1, v2)
        return (op_str, v1, v2)


def inverse(op):
    match op:
        case '+':
            return '-'
        case '-':
            return '+'
        case '*':
            return '/'
        case '/':
            return '*'


def solve(lhs, rhs):
    if lhs == 'x':
        print(f'{lhs} = {rhs}')
        return rhs
    print(f'{lhs} = {rhs} =>')

    if isinstance(lhs, int):
        return solve(rhs, lhs)

    op_str, a, b = lhs
    inv_op_str = inverse(op_str)
    inv_op = get_operator(inv_op_str)
    if op_str in {'*', '+'}:
        if isinstance(a, int):
            return solve(b, inv_op(rhs, a))
        else:
            return solve(a, inv_op(rhs, b))
    else:
        if isinstance(a, int):
            return solve(a, (inv_op_str, rhs, b))
        else:
            return solve(a, inv_op(rhs, b))


def part1(input):
    monkeys = parse_input(input)
    
    root_value = evaluate('root', monkeys)
    
    return root_value


def part2(input):
    monkeys = parse_input(input)
    op, m1, m2 = monkeys['root']
    monkeys['root'] = ('=', m1, m2)
    monkeys['humn'] = 'x'

    lhs, rhs = evaluate('root', monkeys)
    solution = solve(lhs, rhs)

    return solution


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
