import math
import re
import time
from collections import deque
from heapq import heappop, heappush, heapify
from itertools import permutations, product


def shortest_path_to_other_for_valve(valve, graph):
    pq = [(0, valve, '')]
    heapify(pq)
    visited = set()
    d = {v: math.inf for v in graph.keys()}
    d[valve] = 0

    while pq:
        dist, current_valve, path = heappop(pq)

        if current_valve in visited:
            continue

        visited.add(current_valve)

        for v in graph[current_valve][1]:
            next_dist = dist + 1
            if next_dist < d[v]:
                d[v] = next_dist
                heappush(pq, (next_dist, v, path))

    return valve, d['AA'], d


def get_input():
    graph = {}
    with open('input') as file:
        for line in file:
            split = line.strip().split()
            node = split[1]
            flow = int(re.findall(r'[+-]?\d+', split[4])[0])
            adj = [i.split(',')[0] for i in split[9:]]
            graph[node] = (flow, adj)

    # init planar graph
    shortest_paths = []
    map_to_idx = {}

    idx = 0
    # find the shortest path for each node with flow rate
    for key, value in graph.items():
        if value[0] != 0:
            shortest_paths.append(shortest_path_to_other_for_valve(key, graph))
            map_to_idx[key] = idx
            idx += 1

    # map node -> index in final graph
    final_graph = []
    for i in range(len(shortest_paths)):
        adj = []
        valve = shortest_paths[i][0]
        start_time = shortest_paths[i][1]
        min_dist = shortest_paths[i][2]
        pressure = graph[valve][0]
        for v, j in map_to_idx.items():
            if i != j and min_dist[v] != math.inf:
                adj.append((j, min_dist[v] + 1))

        final_graph.append((valve, start_time + 1, pressure, adj))

    print('Graph length', len(final_graph))
    return final_graph


def find_max_remaining_cost_p1(current, graph):
    idx, time, time_spent, pressure, bitmask = current

    flow = time_spent * pressure
    pressure += graph[idx][2]

    ans = flow + (30 - time) * pressure

    # visit adj
    for i, t in graph[idx][3]:
        next_time = time + t
        if not (bitmask & (1 << i)) and next_time <= 30:
            ans = max(ans,
                      flow + find_max_remaining_cost_p1((i, next_time, t, pressure, bitmask | 1 << i), graph))

    return ans


def part1(graph):
    mask = 1 << len(graph)
    ans = 0
    for idx, node in enumerate(graph):
        ans = max(ans, find_max_remaining_cost_p1((idx, node[1], node[1], 0, mask | 1 << idx), graph))

    return ans


id = 0
az = 0


def find_max_remaining_cost(current, graph, dp):
    p_idx, e_idx, time, time_left, pressure, rem_p, rem_e, bitmask_covered = current

    memo = (p_idx, e_idx, time_left, bitmask_covered)

    global id
    global az

    # flow until this minute
    flow = time_left * pressure

    if memo in dp:
        if id % 500_000 == 0:
            print(f'DP HIT {id} :: size={len(dp)}, ans={az}')
        id += 1
        return dp[memo]

    person_opens = p_idx is not None and rem_p == 0
    elephant_opens = e_idx is not None and rem_e == 0

    # calculate pressure for next flow

    if person_opens:
        pressure += graph[p_idx][2]

    if elephant_opens:
        pressure += graph[e_idx][2]

    # calculate until the end using next pressure (t = 24 -> next : 25, 26)
    ans = (26 - time) * pressure

    finished = [(None, math.inf)]

    if rem_p > 0:
        person_next = [(p_idx, rem_p)]
    else:
        person_next = [(i, t) for i, t in graph[p_idx][3] if
                       not (bitmask_covered & (1 << i))] if p_idx is not None else []

    if rem_e > 0:
        elephant_next = [(e_idx, rem_e)]
    else:
        elephant_next = [(i, t) for i, t in graph[e_idx][3] if
                         not (bitmask_covered & (1 << i))] if e_idx is not None else []

    if not person_next and not elephant_next:
        ans = flow + ans
        dp[memo] = ans
        az = max(az, ans)
        return ans

    if not person_next:
        person_next = finished

    if not elephant_next:
        elephant_next = finished

    # if path1.startswith('JJ->JJ->BB->CC') and path2.startswith('DD->HH->HH->EE'):
    #     print(person_next, elephant_next)

    for (i, t1), (j, t2) in product(person_next, elephant_next):
        t = min(t1, t2)
        next_time = time + t
        if i != j and next_time <= 26:
            mask_i = (1 << i) if i is not None else 0
            mask_j = (1 << j) if j is not None else 0
            next = (i, j, next_time, t, pressure, t1 - t, t2 - t, bitmask_covered | mask_i | mask_j)
            ans = max(ans, find_max_remaining_cost(next, graph, dp))

    # if path1.startswith('JJ') and path2.startswith('DD'):
    #
    #     print(
    #         f'== Minute {time} RES={app} :: person_path={path1}, elephant_path={path2}, remaining_time_person={rem_p}, remaining_time_elephant={rem_e} flow={flow}, until_26_flow={ans}, pressure={pressure}, bitmask_covered={bitmask_covered}')

    # f(current) = flow + f(adj, t + 1)
    # f(person_node, elephant_node, bitmask, t) = last_node with next set bitmask, at time t
    ans = flow + ans
    dp[memo] = ans
    az = max(az, ans)
    return ans


def find_max_remaining_cost_seq(current, graph, dp):
    # global id
    # global az
    # id += 1
    # if id % 500_000 == 0:
    #     print(f'id={id}, ans={az}')

    idx, time, bitmask, is_person = current

    if current in dp:
        return dp[current]

    pressure = graph[idx][2]
    flow = (26 - time) * pressure
    ans = 0

    # visit adj
    for i, t in graph[idx][3]:
        next_time = time + t
        if not (bitmask & (1 << i)) and next_time <= 26:
            ans = max(ans, find_max_remaining_cost_seq((i, next_time, bitmask | 1 << i, is_person), graph, dp))

    if is_person:
        for i, node in enumerate(graph):
            if not (bitmask & (1 << i)):
                ans = max(ans, find_max_remaining_cost_seq((i, node[1], bitmask | 1 << i, False), graph, dp))

    dp[current] = flow + ans
    return flow + ans


def part2(graph):
    mask = 1 << len(graph)
    full_mask = (1 << (len(graph) + 1)) - 1
    print(mask, full_mask)
    ans = 0
    print('Graph', graph)
    dp = {}

    for idx, node in enumerate(graph):
        ans = max(ans, find_max_remaining_cost_seq((idx, node[1], mask | 1 << idx, True), graph, dp))

    return ans

    # for i, person in enumerate(graph):
    #     for j, elephant in enumerate(graph):
    #         if i != j:
    #             # p_idx, e_idx, time, time_spent, pressure, rem_p, rem_e, bitmask_rem, valve_p, valve_e, path1, path2
    #             t = min(person[1], elephant[1])
    #             cost = find_max_remaining_cost(
    #                 (i, j, t, t, 0, person[1] - t, elephant[1] - t, mask | 1 << i | 1 << j), graph, dp)
    #             ans = max(ans, cost)


inp = get_input()
start = time.time()
# print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
print(time.time() - start)
