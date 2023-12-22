#!/usr/bin/env python3 -u

"""
First attempt using Dijkstra, but it does not work properly.
It only finds one path but not neccessarily the shortest under the constraint of 3 steps.
"""

import sys
import heapq
from math import inf


OFFSETS = {'L': (0, -1), 'U': (-1, 0), 'R': (0, 1), 'D': (1, 0)}


def neighbours(node: tuple[int, int], grid: list(), to_visit: set()):
    max_x_size = len(grid)
    max_y_size = len(grid[0])


    for direction, offset in OFFSETS.items():
        test_neighbour = tuple(a + b for a, b in zip(node, offset))
        test_x = test_neighbour[0]
        test_y = test_neighbour[1]
        if test_x < 0 or test_x >= max_x_size or test_y < 0 or test_y >= max_y_size:
            continue
        elif test_neighbour in to_visit:
            yield direction, test_neighbour



def main():
    filename = sys.argv[1]

    grid = list()

    with open(filename, 'r') as file:
        for line in file:
            grid.append(line.strip())

    # print(grid)


    start_node = (0, 0)
    final_node = (len(grid)-1, len(grid[0])-1)

    dist = dict()
    heap_dist = list()
    prev = dict()
    Q = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dist[(i, j)] = inf
            prev[(i, j)] = {'last_node': None, 'last_direction': None, 'step_in_direction':0}
            Q.add((i, j))

    dist[start_node] = 0
    heapq.heappush(heap_dist, (0, start_node))

    while Q:
        explore = heapq.heappop(heap_dist)
        cur_min_dist = explore[0]
        cur_node = explore[1]
        print(f"Exploring {cur_node} because it has min distance to start node of {cur_min_dist}.")
        
        Q.remove(cur_node)
        
        for direction, neighbour in neighbours(cur_node, grid, Q):
            print(f"Updating its neighbour {neighbour}")

            if prev[cur_node]['last_direction'] == direction and prev[cur_node]['step_in_direction'] == 3:
                print(f"On direction {direction}, there have been 3 steps.")
                continue

            alt = cur_min_dist + int(grid[neighbour[0]][neighbour[1]])
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                prev[neighbour]['last_node'] = cur_node
                prev[neighbour]['last_direction'] = direction
                if prev[cur_node]['last_direction'] == direction:
                    prev[neighbour]['step_in_direction'] = prev[cur_node]['step_in_direction'] + 1
                else:
                    prev[neighbour]['step_in_direction'] = 1
                heapq.heappush(heap_dist, (alt, neighbour))

    print(f"Final node {final_node} has distance of {dist[final_node]} to the start node.")


    last_node = prev[final_node]['last_node']
    trace = f"{final_node} -> {last_node}"
    while last_node != start_node:
        last_node = prev[last_node]['last_node']
        trace += f" -> {last_node}"

    print(trace)

if __name__ == "__main__":
    main()