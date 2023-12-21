#!/usr/bin/env python3 -u

import sys
import heapq
from math import inf


# 0: Up; 1: Right; 2: Down; 3: Left
OFFSETS = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


def neighbours(node: tuple[int, int], grid: list()):
    max_x_size = len(grid)
    max_y_size = len(grid[0])

    for direction, offset in OFFSETS.items():
        test_neighbour = tuple(a + b for a, b in zip(node, offset))
        test_x = test_neighbour[0]
        test_y = test_neighbour[1]
        if test_x < 0 or test_x >= max_x_size or test_y < 0 or test_y >= max_y_size:
            continue
        else:
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

    Q = list()
    heapq.heappush(Q, (0, start_node, -1, 0))

    visited = dict()

    while Q:
        cur_min_dist, cur_node, last_direction, step_in_direction = heapq.heappop(Q)
        # print(f"Exploring {cur_node} because it has min distance to start node of {cur_min_dist}.")
        
        if (cur_node, last_direction, step_in_direction) in visited:
            continue
        else:
            visited[(cur_node, last_direction, step_in_direction)] = cur_min_dist
        
        for direction, neighbour in neighbours(cur_node, grid):
            # print(f"Updating its neighbour {neighbour}")

            if last_direction == direction and step_in_direction == 3:
                # print(f"On direction {direction}, there have been 3 steps.")
                continue

            if (direction + 2) % 4 == last_direction:
                # print(f"Reverse direction")
                continue

            alt = cur_min_dist + int(grid[neighbour[0]][neighbour[1]])
            if last_direction == direction:
                new_step = step_in_direction + 1
            else:
                new_step = 1
            heapq.heappush(Q, (alt, neighbour, direction, new_step))
        
            # print(visited)


    for (node, last_direction, step_in_direction), v in visited.items():
        if node == final_node:
            print(f"Final node {final_node} has distance of {v} to the start node.")


if __name__ == "__main__":
    main()