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


sys.setrecursionlimit(10**2)

MAX_STEPS = 0
COUNT = 0

def dfs(cur_v: tuple(), distance: int, path: list(), destination: tuple(), E: dict(), mode: str):
    global MAX_STEPS
    global COUNT

    if cur_v in path:
        return

    if cur_v == destination:
        COUNT += 1
        MAX_STEPS = max(distance, MAX_STEPS)
        print(f"{COUNT=} {MAX_STEPS=}")
        return
    
    if mode == 'vanila':
        # Vanila recursion, no preference of d
        for next_v, d in E[cur_v].items():
            new_path = copy.deepcopy(path)
            new_path.append(cur_v)
            dfs(next_v, distance+d, new_path, destination, E, mode)
    elif mode == 'greedy':
        # Prefer explore the largest d first
        cur_E = copy.deepcopy(E[cur_v])
        while cur_E:
            max_d = max(cur_E.values())
            for next_v, d in cur_E.items():
                if d == max_d:
                    new_path = copy.deepcopy(path)
                    new_path.append(cur_v)
                    dfs(next_v, distance+d, new_path, destination, E, mode)
            del cur_E[next_v]
 


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

    logging.debug(f"{len(V)=} {V=}")
    for v, e in E.items():
        logging.debug(f"{len(e)=} {v=} {e=}")

    mode = 'greedy'
    # DFS 
    dfs(start, 0, [], final, E, mode)


if __name__ == "__main__":
    main()