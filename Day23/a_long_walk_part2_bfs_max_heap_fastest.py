#!/usr/bin/env python3 -u

import sys
import copy
import heapq
from collections import deque
import logging

"""
Reduced big map to small maps segragated by crossing points 
where the number of neighbours are greater than 2

These points consist of a Vertex set V
Their distances to each other consist of an Edge set E
"""

logging.basicConfig(level=logging.INFO, filemode='w')

SLOPES = ('^', '>', 'v', '<')
OFFSETS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def main():
    filename = sys.argv[1]

    grid = list()

    with open(filename, 'r') as file:
        for line in file:
            grid.append(line.strip())

    logging.debug(f"{grid=}")

    start = (0, 1)
    final = (len(grid)-1, len(grid[0])-2)

    V = list()
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            nbr = 0
            for dx, dy in OFFSETS:
                if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                    if grid[x+dx][y+dy] != '#':
                        nbr += 1
            if nbr > 2 and grid[x][y] != '#':
                V.append((x, y))
    
    V = [start] + V
    V = V + [final]

    E = dict()
    for cur_x, cur_y in V:
        E[(cur_x, cur_y)] = dict()
        Q = []
        heapq.heappush(Q, (0, cur_x, cur_y))
        visited = set()
        while Q:
            d, x, y = heapq.heappop(Q)
            
            if (x, y) in visited:
                continue
            
            # Stop at another vertex that has more than 2 routes
            # Won't extend anymore
            if (x, y) in V and (x, y) != (cur_x, cur_y):
                # Add it to the edge map
                E[(cur_x, cur_y)][(x, y)] = d
                continue
            
            for idx, (dx, dy) in enumerate(OFFSETS):
                if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                    if grid[x+dx][y+dy] == '#':
                        continue
                    heapq.heappush(Q, (d+1, x+dx, y+dy))
            
            visited.add((x, y))

    logging.debug(f"{V=}")
    for v, e in E.items():
        logging.debug(f"{v=} {e=}")


    # BFS with max heap 
    # Equivalent to a DFS
    queue = []
    heapq.heappush(queue, (0, start, []))

    final_steps = []

    count = 0
    while queue:
        count += 1
        if count % 10000 == 0:
            print(f"{count=}")

        steps, cur_v, path = heapq.heappop(queue)
        
        if cur_v in path:
            continue
        
        if cur_v == final:
            final_steps.append(steps)
            max_steps = min(final_steps)
            print(f"{max_steps=}")
            continue

        for next_v, d in E[cur_v].items():
            if next_v in path:
                continue
            new_path = copy.deepcopy(path)
            new_path.append(cur_v)

            # Use negative steps to simulate max heap
            heapq.heappush(queue, (steps-d, next_v, new_path))

    max_steps = min(final_steps)
    print(f"{max_steps=} {final_steps=}")


if __name__ == "__main__":
    main()