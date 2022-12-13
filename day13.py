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
        # if self.type == 'int':
        #     return f'int:{self.value}'
        return str(self.value).replace(' ', '')

    # def __lt__(self, other):
    #     if self.type == 'int' and other.type == 'int':
    #         return self.value < other.value
    #     elif self.type == 'list' and other.type == 'list':
    #         return all([l < r for l, r in zip(self.value, other.value)]) and len(self.value) <= len(other.value)
    #     elif self.type == 'int':
    #         return Packet('[' + str(self.value) + ']') < other
    #     else:
    #         return self < Packet('[' + str(other.value) + ']')


    def __lt__(self, other):
        print(f'Compare {self} and {other}')
        if self.type == 'int' and other.type == 'int':
            return self.value < other.value
        elif self.type == 'list' and other.type == 'list':
            for l, r in zip(self.value, other.value):
                if l < r:
                    return True
                elif r < l:
                    return False
            print(self.value, other.value, 'are the same')
            return len(self.value) < len(other.value)
        elif self.type == 'int':
            return Packet('[' + str(self.value) + ']') < other
        else:
            return self < Packet('[' + str(other.value) + ']')


def part1(input):
    counter = 0
    for line_number, line in enumerate(read_input_simple(13, input)):
        match line_number % 3:
            case 0:
                left_packet = Packet(line)
            case 1:
                right_packet = Packet(line)
            case 2:
                print(left_packet)
                print(right_packet)
                if left_packet < right_packet:
                    print('correct order')
                    counter += line_number // 3 + 1
                else:
                    print('wrong order')
                print()
    return counter


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
