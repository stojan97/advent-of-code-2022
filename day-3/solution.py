def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]
    return lines


PRIORITY = {}
for i in range(1, 27):
    PRIORITY[chr(i + 96)] = i
    PRIORITY[chr(i + 64)] = i + 26


def part1(rucksacks):
    total = 0
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        first, second = rucksack[:half], rucksack[half:]
        total += PRIORITY[''.join(set(first) & set(second))]

    return total


def part2(rucksacks):
    total = 0
    for i in range(0, len(rucksacks), 3):
        intersection = set(rucksacks[i]) & set(rucksacks[i + 1]) & set(rucksacks[i + 2])
        total += PRIORITY[''.join(intersection)]

    return total


inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
