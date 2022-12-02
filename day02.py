from helper.input import read_input
import sys


def game_score(their_letter, my_letter):
    if beats[their_letter] == my_letter:
        return 6
    elif beats[my_letter] == their_letter:
        return 0
    else:
        return 3


def part1(input):
    total_score = 0
    for [a, b] in read_input(2, input, [(str,)]):
        a_numeric = ord(a) - ord('A')
        b_numeric = ord(b) - ord('X')
        game_score = 3 + ((4 + b_numeric - a_numeric) % 3 - 1) * 3
        letter_score = b_numeric + 1
        total_score += game_score + letter_score
    return total_score


def part2(input):
    total_score = 0
    for [a, b] in read_input(2, input, [(str,)]):
        a_numeric = ord(a) - ord('A')
        b_numeric = ord(b) - ord('X')
        game_score = 3 + (b_numeric - 1) * 3
        letter_score = (2 + b_numeric + a_numeric) % 3 + 1
        total_score += game_score + letter_score
    return total_score


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
