def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]
    return lines[0]


def solve(input, distinct_chars):
    for i in range(len(input) - distinct_chars):
        current = input[i: i + distinct_chars]
        if len(set(current)) == distinct_chars:
            return i + distinct_chars

    return -1


inp = get_input()
print('Part 1:', solve(inp, 4))
print('Part 2:', solve(inp, 14))
