def get_input():
    pairs = []
    with open('input') as file:
        for line in file:
            split = line.strip().split(',')
            first_pair = split[0].split('-')
            second_pair = split[1].split('-')
            pairs.append(((int(first_pair[0]), int(first_pair[1])), (int(second_pair[0]), int(second_pair[1]))))

    return pairs


def solve(pairs, get_rule):
    return sum(get_rule(first, second) for first, second in pairs)


def part1_fully_contain_rule(first, second):
    mini = min(first[0], second[0])
    maxi = max(first[1], second[1])
    return int((mini == first[0] and maxi == first[1]) or (mini == second[0] and maxi == second[1]))


def part2_intersection_rule(first, second):
    mini = max(first[0], second[0])
    maxi = min(first[1], second[1])
    return int(mini <= maxi)


inp = get_input()
print('Part 1:', solve(inp, part1_fully_contain_rule))
print('Part 2:', solve(inp, part2_intersection_rule))
