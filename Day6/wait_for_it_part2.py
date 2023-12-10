#!/usr/bin/env python3 -u

# D: Distance; R: Record; T: total Time
# x: time to hold
# D - R = - x^2 + Tx - R > 0
# x = (T +/- sqrt(T^2 - 4R)) / 2

import math


def main():
    filename = "original_input"

    values = list()

    with open(filename, 'r') as file:
        for line in file:
            values.append(int(''.join(line.split(':')[1].strip().split())))

    # print(f"values: {values}")
    # values = list(zip(*values))

    res = 1
    
    T = values[0]
    R = values[1]
    min_hold = math.floor((T - math.sqrt(pow(T, 2) - 4 * R)) / 2)
    max_hold = math.ceil((T + math.sqrt(pow(T, 2) - 4 * R)) / 2)

    res = res * (max_hold - min_hold - 1)

    print(f"res: {res}")


if __name__ == "__main__":
    main()