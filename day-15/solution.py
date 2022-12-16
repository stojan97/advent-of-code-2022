import re
import time


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_input():
    lines = []
    sensors = []
    beacons = set()

    with open('input') as file:
        for line in file:
            points = re.findall(r'[+-]?\d+', line.strip())
            lines.append(points)
            sensor_pos = (int(points[1]), int(points[0]))
            beacon_pos = (int(points[3]), int(points[2]))
            coverage = dist(sensor_pos, beacon_pos)
            sensors.append((sensor_pos[0], sensor_pos[1], coverage))
            beacons.add(beacon_pos)

    return sensors, beacons


def get_merged_intervals(intervals):
    intervals.sort()
    merged = []

    for interval in intervals:
        if not merged:
            merged.append(interval)
            continue

        if interval[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
        else:
            merged.append(interval)

    return merged


def get_answer_from_intervals(intervals):
    intervals.sort()
    prev_end = intervals[0][1]

    for start, end in intervals[1:]:
        if start > prev_end:
            return prev_end + 1

        prev_end = max(prev_end, end)

    return None


def get_interval_from_row(sensor, row):
    x, y, coverage = sensor

    intersecting_point = (row, y)
    distance = dist((x, y), intersecting_point)

    if distance > coverage:
        return None

    spread = coverage - distance

    return y - spread, y + spread


def get_intervals(sensors, row, merge_callback):
    intervals = []
    for sensor in sensors:
        interval = get_interval_from_row(sensor, row)
        if interval:
            intervals.append(interval)

    return merge_callback(intervals)


def part1(input):
    sensors, beacons = input
    row = 2_000_000
    merged_intervals = get_intervals(sensors, row, lambda intervals: get_merged_intervals(intervals))
    spread_intervals = sum(m_interval[1] - m_interval[0] + 1 for m_interval in merged_intervals)
    beacons_on_row = sum(int(beacon[0] == row) for beacon in beacons)

    return spread_intervals - beacons_on_row


def part2(input):
    sensors, beacons = input
    limit = 4_000_000
    tuning_freq_mul = 4_000_000
    merge = lambda i: get_answer_from_intervals(i)

    for row in range(limit + 1):
        answer = get_intervals(sensors, row, merge)
        if row % 100_000 == 0:
            print(f'Row: {row} ::: answer={answer}')

        if answer:
            return answer * tuning_freq_mul + row

    return -1


inp = get_input()
print('Part 1:', part1(inp))
start = time.time()
# 30 secs
print('Part 2:', part2(inp))
print(time.time() - start)
