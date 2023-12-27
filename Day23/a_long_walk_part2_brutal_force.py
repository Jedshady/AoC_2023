#!/usr/bin/env python3 -u

import sys
import copy
import heapq
from collections import deque
import logging

"""
The graph is way too big to find answer by brutal force on each <x, y>.
The longest path is an NP problem.
Need to find some specialties about the graph to reduce the complexity.
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

    logging.debug(f"{start=} {final=}")

    queue = []
    heapq.heappush(queue, (0, start[0], start[1], set()))

    final_steps = []

    count = 0
    while queue:
        count += 1
        if count % 10000 == 0:
            print(f"{count=}")

        logging.debug(f"{queue=}")
        steps, x, y, path = heapq.heappop(queue)

        logging.debug(f"{steps=} {x=} {y=}")

        if (x, y) == final:
            final_steps.append(steps)
            print(f"Found a path, {steps=}")
            max_step = min(final_steps)
            print(f"{max_step=}")

    
        for idx, (dx, dy) in enumerate(OFFSETS):
            if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                logging.debug(f"Testing {x+dx=} {y+dy=}")
                if (x+dx, y+dy) in path:
                    logging.debug(f"Found in path")
                    continue

                if grid[x+dx][y+dy] == '#':
                    logging.debug(f"Skip #")
                    continue

                # split_path = copy.deepcopy(path)
                # split_path.append((x,y))
                # heapq.heappush(queue, (steps-1, x+dx, y+dy, split_path))

                new_path = path | {(x, y)}
                heapq.heappush(queue, (steps-1, x+dx, y+dy, new_path))

        # if count == 1500:
        #     break


    print(f"{final_steps=}")
    max_step = min(final_steps)

    print(max_step)




if __name__ == "__main__":
    main()