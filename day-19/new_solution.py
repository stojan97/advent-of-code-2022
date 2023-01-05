import re
import time
from functools import cmp_to_key


def get_numbers(str):
    return list(map(int, re.findall(r'\d+', str)))


def get_input():
    blueprints = []
    with open('input') as file:
        id = 1
        for line in file:
            # 0 - ore
            # 1 - clay
            # 2 - obsidian
            # 3 - geode
            strip = line.strip().split('. ')
            costs = [0, 0, 0, 0]
            ore_costs = get_numbers(strip[0].split('Each ')[1])
            costs[0] = {0: ore_costs[0]}
            clay_costs = get_numbers(strip[1].split('Each ')[1])
            costs[1] = {0: clay_costs[0]}
            obsidian_costs = get_numbers(strip[2].split('Each ')[1])
            costs[2] = {0: obsidian_costs[0], 1: obsidian_costs[1]}
            geode_costs = get_numbers(strip[3].split('Each ')[1])
            costs[3] = {0: geode_costs[0], 2: geode_costs[1]}

            blueprint = (id, costs)
            blueprints.append(blueprint)
            id += 1

    return blueprints


def get_time_increment(cost, robots, rocks):
    remaining = cost - rocks
    if robots == 0:
        return None

    if remaining <= 0:
        return 1

    next_time_increment = remaining // robots + int(remaining % robots != 0)
    return next_time_increment + 1


def get_max_time_increment(costs, robots, rocks):
    time_increment = 0
    for rock, cost in costs.items():
        increment = get_time_increment(cost, robots[rock], rocks[rock])
        if increment is None:
            return None
        time_increment = max(time_increment, increment)

    return time_increment


def next_robot(val, r_i, i):
    return val + int(r_i == i)


def next_rocks(rock, robots, i, cost, time_increment):
    value = (rock + (time_increment * robots))
    return value - cost[i] if i in cost else value


def get_next_state(i, robots, rocks, cost, time_increment):
    new_robots = (
        next_robot(robots[0], 0, i),
        next_robot(robots[1], 1, i),
        next_robot(robots[2], 2, i),
        next_robot(robots[3], 3, i)
    )
    new_rocks = (
        next_rocks(rocks[0], robots[0], 0, cost, time_increment),
        next_rocks(rocks[1], robots[1], 1, cost, time_increment),
        next_rocks(rocks[2], robots[2], 2, cost, time_increment),
        next_rocks(rocks[3], robots[3], 3, cost, time_increment)
    )

    return new_robots, new_rocks


counter = 1
ans = 0


def max_state(s1, s2):

    if s1[0] == s2[0]:
        return -1 if s1[1][::-1] >= s2[1][::-1] else 1

    return -1 if s1[0][::-1] > s2[0][::-1] else 1


def solve_rock(state, dp, LIMIT, costs, memo, rock_type, init):
    robots, rocks, time = state

    global counter

    if counter % 500_000 == 0:
        print(f'hits={counter} === State={state}, dp={len(dp)}')
    counter += 1

    if init == rock_type:
        memo[rock_type][time].append((robots, rocks))

    if time == LIMIT:
        return

    start = rock_type if init != rock_type else max(0, rock_type - 1)

    for i in range(start, rock_type + 1):
        # check next robot build
        time_increment = get_max_time_increment(costs[i], robots, rocks)
        if time_increment is None:
            break

        next_time = time + time_increment
        if next_time <= LIMIT:
            r, c = get_next_state(i, robots, rocks, costs[i], time_increment)
            next_state = (r, c, next_time)
            if next_state not in dp:
                dp.add(next_state)
                solve_rock(next_state, dp, LIMIT, costs, memo, rock_type, rock_type)


def solve_geode(state, dp, LIMIT, costs, init):
    robots, rocks, time = state

    global counter

    if counter % 500_000 == 0:
        print(f'===== geode-collecting robot ===== hits={counter} === State={state}, dp={len(dp)}')
    counter += 1

    geode = rocks[3] + (LIMIT - time) * robots[3]
    global ans
    ans = max(ans, geode)

    if time == LIMIT:
        return

    start = 3 if init else 2

    for i in range(start, 4):
        # check next robot build
        time_increment = get_max_time_increment(costs[i], robots, rocks)
        if time_increment is None:
            break
        next_time = time + time_increment
        if next_time <= LIMIT:
            r, c = get_next_state(i, robots, rocks, costs[i], time_increment)
            next_state = (r, c, next_time)
            if next_state not in dp:
                dp.add(next_state)
                solve_geode(next_state, dp, LIMIT, costs, False)


def solve_part(blueprints, LIMIT, s, f):

    for id, costs in blueprints:
        global ans
        ans = 0
        global counter

        memo = [{}, {}, {}, {}]

        for t in range(1, LIMIT + 1):
            for j in range(4):
                memo[j][t] = []

        print('========== ore collecting robot ===========')
        dp = set()
        counter = 0
        solve_rock(((1, 0, 0, 0), (0, 0, 0, 0), 1), dp, LIMIT, costs, memo, 0, 0)

        print()
        counter = 0
        print('========== clay collecting robot | starting from ore ===========')
        for t, c in memo[0].items():
            sliced = sorted(c, key=cmp_to_key(max_state))[:(t * t)]
            print(f'Time {t} :: REAL_LENGTH={len(c)} ==== {len(sliced)}')
            for robots, rocks in sliced:
                solve_rock((robots, rocks, t), dp, LIMIT, costs, memo, 1, 0)

        print()
        counter = 0
        print('========== obsidian collecting robot | starting from clay ===========')
        for t, c in memo[1].items():
            sliced = sorted(c, key=cmp_to_key(max_state))[:(t * t)]
            print(f'Time {t} :: REAL_LENGTH={len(c)} ==== {len(sliced)}')
            for robots, rocks in sliced:
                solve_rock((robots, rocks, t), dp, LIMIT, costs, memo, 2, 1)

        print()
        counter = 0
        print('========== geode collecting robot starting from obsidian ===========')
        for t, c in memo[2].items():
            sliced = sorted(c, key=cmp_to_key(max_state))[:(t * t)]
            print(f'Time {t} :: REAL_LENGTH={len(c)} ==== {len(sliced)}')
            for robots, rocks in sliced:
                solve_geode((robots, rocks, t), dp, LIMIT, costs, True)

        print()
        print('========== geode Results ===========')
        s = f(s, id, ans)
        print(f'Blueprint {id} => {ans}')

    return s


inp = get_input()
start = time.time()
print('Part 1:', solve_part(inp, 25, 0, lambda s, id, ans: s + (id * ans)))
print('Part 2:', solve_part(inp[:3], 33, 1, lambda s, id, ans: s * ans))
print(time.time() - start)
