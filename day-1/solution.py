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


input = get_input()


def part1():
    return max(sum(i) for i in input)


def part2():
    return sum(sorted([sum(i) for i in input], reverse=True)[:3])


print('Part 1:', part1())
print('Part 2:', part2())
