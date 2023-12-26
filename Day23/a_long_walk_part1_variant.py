#!/usr/bin/env python3 -u

import sys
import copy
import heapq
from collections import deque
import logging

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

    logging.debug(f"{start=} {final=}")

    queue = []
    heapq.heappush(queue, (0, start[0], start[1], set()))

    final_steps = []
    point_to_max_steps = dict()

    while queue:
        logging.debug(f"{queue=}")
        steps, x, y, path = heapq.heappop(queue)

        logging.debug(f"{steps=} {x=} {y=}")

        if (x, y) == final:
            final_steps.append(steps)
            print(f"Found a path, {steps=}")

        # Use a dict to store current max steps on a point.
        # In order to avoid search too broad
        if (x, y) in point_to_max_steps and point_to_max_steps[(x, y)] <= steps:
            continue
        else: 
            point_to_max_steps[(x, y)] = steps

        # if steps == 18:
        #     break
    
        if grid[x][y] in SLOPES:
            path.add((x, y))
            idx = SLOPES.index(grid[x][y])
            dx, dy = OFFSETS[idx]
            heapq.heappush(queue, (steps-1, x+dx, y+dy, path))
            continue

        for idx, (dx, dy) in enumerate(OFFSETS):
            if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                logging.debug(f"Testing {x+dx=} {y+dy=}")
                if (x+dx, y+dy) in path:
                    logging.debug(f"Found in path")
                    continue

                if grid[x+dx][y+dy] == '#':
                    logging.debug(f"Skip #")
                    continue

                if grid[x+dx][y+dy] in SLOPES:
                    if (idx + 2) % 4 == SLOPES.index(grid[x+dx][y+dy]):
                        logging.debug(f"Blocked by slope")
                        continue
                    
                new_path = path | {(x, y)}
                heapq.heappush(queue, (steps-1, x+dx, y+dy, new_path))

    print(f"{final_steps=}")
    max_step = min(final_steps)

    print(max_step)
    # print(point_to_max_steps)




if __name__ == "__main__":
    main()