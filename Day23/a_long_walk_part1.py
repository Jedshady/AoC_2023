#!/usr/bin/env python3 -u

import sys
import heapq
import copy
import time
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
    heapq.heappush(queue, (0, start[0], start[1], []))

    steps_to_path = dict()

    while queue:
        logging.debug(f"{queue=}")
        steps, x, y, path = heapq.heappop(queue)

        logging.debug(f"{steps=} {x=} {y=}")

        if (x, y) == final:
            steps_to_path[steps] = path
            print(f"Found a path, {abs(steps)=}")    

        # if steps == 18:
            # break
    
        if grid[x][y] in SLOPES:
            path.append((x, y))
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
                    
                split_path = copy.deepcopy(path)
                split_path.append((x,y))
                heapq.heappush(queue, (steps-1, x+dx, y+dy, split_path))

    max_step = 0
    for steps, path in steps_to_path.items():
        logging.debug(f"{steps=} {path=}")
        max_step = min(max_step, steps)

    print(abs(max_step))




if __name__ == "__main__":
    main()