from helper.input import read_input_simple
import sys


class Packet:
    @staticmethod
    def find_end(string):
        first_comma = string.find(',')
        first_bracket = string.find(']')
        if first_comma == -1 and first_bracket == -1:
            return len(string)
        elif first_comma != -1 and first_bracket != -1:
            if first_comma < first_bracket:
                return first_comma
            else:
                return first_bracket
        elif first_comma == -1:
            return first_bracket
        else:
            return first_comma


    def __init__(self, string):
        self.string = string
        if string[0] == '[':
            depth = 0
            matching_bracket = -1
            for index, c in enumerate(string[1:]):
                if depth == 0 and c == ']':
                    matching_bracket = index + 1
                    break
                elif c == '[':
                    depth += 1
                elif c == ']':
                    depth -= 1
            self.type = 'list'
            self.end = matching_bracket + Packet.find_end(string[matching_bracket + 1:]) + 1
            self.value = []
            start_index = 1
            while start_index < matching_bracket:
                sub_packet = Packet(string[start_index:self.end])
                self.value.append(sub_packet)
                start_index = sub_packet.end + start_index + 1
        elif string[0].isdigit():
            self.type = 'int'
            self.end = Packet.find_end(string)
            self.value = int(string[:self.end])
        else:
            print(f'No match for: {string}')
            

    def __repr__(self):
        return str(self.value).replace(' ', '')


    def __lt__(self, other):
        if self.type == 'int' and other.type == 'int':
            return self.value < other.value
        elif self.type == 'list' and other.type == 'list':
            for l, r in zip(self.value, other.value):
                if l < r:
                    return True
                elif r < l:
                    return False
            return len(self.value) < len(other.value)
        elif self.type == 'int':
            return Packet('[' + str(self.value) + ']') < other
        else:
            return self < Packet('[' + str(other.value) + ']')


    def __eq__(self, other):
        return self.string == other.string


def part1(input):
    counter = 0
    for line_number, line in enumerate(read_input_simple(13, input)):
        match line_number % 3:
            case 0:
                left_packet = Packet(line)
            case 1:
                right_packet = Packet(line)
            case 2:
                if left_packet < right_packet:
                    counter += line_number // 3 + 1
    return counter


def part2(input):
    packets = [Packet(line) for line in read_input_simple(13, input) if line != '']
    divider1 = Packet('[[2]]')
    divider2 = Packet('[[6]]')
    packets.append(divider1)
    packets.append(divider2)
    packets.sort()
    return (packets.index(divider1) + 1) * (packets.index(divider2) + 1)


if __name__ == '__main__':
    _, part, input = sys.argv
    if part == '1':
        print(part1(input))
    elif part == '2':
        print(part2(input))
    else:
        print('Part must be one of 1 or 2')
