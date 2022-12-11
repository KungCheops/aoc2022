from helper.input import read_input_simple
import sys
from queue import Queue
import operator


ops = {'+': operator.add, '*': operator.mul}


class Monkey:
    def __init__(self, monkey_id, items, operator, operand, divisor, true_target, false_target):
        self.monkey_id = monkey_id
        self.items = items
        self.operator = operator
        self.operand = operand
        self.divisor = divisor
        self.true_target = true_target
        self.false_target = false_target
        self.items_inspected = 0


    def has_next(self):
        return not self.items.empty()


    def get_next(self):
        next_item = self.items.get()
        if self.operand == 'old':
            operand = next_item
        else:
            operand = int(self.operand)
        new_worry_level = self.operator(next_item, operand) // 3
        if new_worry_level % self.divisor == 0:
            target_monkey = self.true_target
        else:
            target_monkey = self.false_target
        self.items_inspected += 1
        return new_worry_level, target_monkey


    def add_item(self, item):
        self.items.put(item)


    def __repr__(self):
        return str(self.items_inspected)


    def __lt__(self, other):
        return self.items_inspected < other.items_inspected


    def __eq__(self, other):
        return self.items_inspected == other.items_inspected


def parse_input(input):
    monkeys = []
    
    for line_number, line in enumerate(read_input_simple(11, input)):
        match line_number % 7:
            case 0:
                monkey_id = line[7]
            case 1:
                monkey_items = Queue()
                for item in map(int, line.replace(',', '').split(' ')[2:]):
                    monkey_items.put(item)
            case 2:
                operator = ops[line.split()[4]]
                operand = line.split()[5]
            case 3:
                divisor = int(line.split()[3])
            case 4:
                true_target = int(line.split()[5])
            case 5:
                false_target = int(line.split()[5])
            case 6:
                # print(monkey_id, monkey_items, operator, operand, divisor, true_target, false_target)
                monkeys.append(Monkey(monkey_id, monkey_items, operator, operand, divisor, true_target, false_target))

    return monkeys


def part1(input):
    monkeys = parse_input(input)

    for i in range(20):
        for monkey in monkeys:
            while monkey.has_next():
                item, target = monkey.get_next()
                # print(f'Monkey {monkey.monkey_id} throws item with worry level {item} to monkey {target}.')
                monkeys[target].add_item(item)

    sorted_monkeys = sorted(monkeys)
    return sorted_monkeys[-1].items_inspected * sorted_monkeys[-2].items_inspected


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
