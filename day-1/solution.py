def get_input():
    lines = []
    new_list = []
    with open('input') as file:

        for line in file:
            line_stripped = line.strip()
            if line_stripped == '':
                lines.append(new_list)
                new_list = []
            else:
                new_list.append(int(line_stripped))

    lines.append(new_list)
    return lines


def part1(input):
    return max(sum(i) for i in input)


def part2(input):
    return sum(sorted([sum(i) for i in input], reverse=True)[:3])


inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
