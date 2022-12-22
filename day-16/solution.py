import math
import re
import time
from heapq import heappop, heappush, heapify


def shortest_path_to_other_for_valve(valve, graph):
    pq = [(0, valve)]
    heapify(pq)
    visited = set()
    d = {v: math.inf for v in graph.keys()}
    d[valve] = 0

    while pq:
        dist, current_valve = heappop(pq)

        if current_valve in visited:
            continue

        visited.add(current_valve)

        for v in graph[current_valve][1]:
            next_dist = dist + 1
            if next_dist < d[v]:
                d[v] = next_dist
                heappush(pq, (next_dist, v))

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
        adj = {}
        valve = shortest_paths[i][0]
        start_time = shortest_paths[i][1]
        min_dist = shortest_paths[i][2]
        pressure = graph[valve][0]
        for v, j in map_to_idx.items():
            if i != j and min_dist[v] != math.inf:
                adj[j] = min_dist[v] + 1

        final_graph.append((valve, start_time + 1, pressure, adj))

    print('Graph length', len(final_graph))
    return final_graph


def find_max_remaining_cost_p1(current, graph, dp):
    idx, time, source, pressure, bitmask = current

    memo = idx, time, source, bitmask

    if memo in dp:
        return dp[memo]

    time_spent = graph[source][3][idx] if source != -1 else graph[idx][1]
    flow = time_spent * pressure
    pressure += graph[idx][2]

    ans = flow + (30 - time) * pressure

    # visit adj
    for i, t in graph[idx][3].items():
        next_time = time + t
        if not (bitmask & (1 << i)) and next_time <= 30:
            ans = max(ans,
                      flow + find_max_remaining_cost_p1((i, next_time, idx, pressure, bitmask | 1 << i), graph, dp))

    dp[memo] = ans
    return ans


def part1(graph):
    mask = 1 << len(graph)
    ans = 0
    dp = {}
    for idx, node in enumerate(graph):
        ans = max(ans, find_max_remaining_cost_p1((idx, node[1], -1, 0, mask | 1 << idx), graph, dp))

    return ans


def find_max_remaining_cost(current, graph, dp):
    idx, time, source, pressure, bitmask, is_person = current

    memo = idx, time, source, pressure, bitmask, is_person

    if memo in dp:
        return dp[memo]

    time_spent = graph[source][3][idx] if source != -1 else graph[idx][1]
    flow = time_spent * pressure
    pressure += graph[idx][2]

    ans = (26 - time) * pressure
    until_end = ans

    for i, t in graph[idx][3].items():
        next_time = time + t
        if not (bitmask & (1 << i)) and next_time <= 26:
            ans = max(ans,
                      find_max_remaining_cost((i, next_time, idx, pressure, bitmask | 1 << i, is_person), graph, dp))

    if is_person:
        for i, node in enumerate(graph):
            if not (bitmask & (1 << i)):
                remaining_cost = find_max_remaining_cost((i, node[1], -1, 0, bitmask | 1 << i, False), graph, dp)
                ans = max(ans, until_end + remaining_cost)

    total = flow + ans
    dp[memo] = total
    return total


def part2(graph):
    mask = 1 << len(graph)
    full_mask = (1 << (len(graph) + 1)) - 1
    print(mask, full_mask)
    ans = 0
    print('Graph', graph)
    dp = {}

    for idx, node in enumerate(graph):
        ans = max(ans, find_max_remaining_cost((idx, node[1], -1, 0, mask | 1 << idx, True), graph, dp))

    return ans


inp = get_input()
start = time.time()
print('Part 1:', part1(inp))
# 1 min 30 secs for worse inputs, and 20 secs for good inputs
print('Part 2:', part2(inp))
print(time.time() - start)
