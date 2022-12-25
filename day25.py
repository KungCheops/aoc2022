from helper.input import read_input_simple
import sys


def decimal_to_snafu(dec):
    a, b = dec, 0
    ret_str = ''
    while a > 0:
        a, b = (a + 2) // 5, (a) % 5
        match b:
            case 3:
                ret_str = '=' + ret_str
            case 4:
                ret_str = '-' + ret_str
            case 0:
                ret_str = '0' + ret_str
            case 1:
                ret_str = '1' + ret_str
            case 2:
                ret_str = '2' + ret_str
    return ret_str


def snafu_to_decimal(snafu):
    val = 0
    for i, char in enumerate(reversed(snafu)):
        match char:
            case '=':
                val -= 2 * (5 ** i)
            case '-':
                val -= 1 * (5 ** i)
            case '1':
                val += 1 * (5 ** i)
            case '2':
                val += 2 * (5 ** i)
    return val
                


def part1(input):
    total = 0
    for snafu in read_input_simple(25, input):
        total += int(snafu_to_decimal(snafu))
    # [print(i, decimal_to_snafu(i)) for i in [1, 2, 3, 4, 5, 11, 25, 27, 24, 23]]
    return decimal_to_snafu(total)


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
