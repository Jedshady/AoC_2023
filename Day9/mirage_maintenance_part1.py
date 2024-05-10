#!/usr/bin/env python3 -u


def calculate_diff(i: int, j: int, input: list[int], diff: list) -> list[list[int]]:
    if diff[i][j] is None:
        if i == 0:
            diff[i][j] = input[j+1] - input[j]
        else:
            diff[i][j] = calculate_diff(i-1, j+1, input, diff) - calculate_diff(i-1, j, input, diff)

    return diff[i][j]


def main():
    filename = "original_input"

    res = list()
    with open(filename, 'r') as file:
        for line in file:
            input = list(map(int, line.split()))
            # print(input)

            diff = [[None for _ in range(len(input)+1)] for i in range(len(input))]
            # print(diff)

            max_level = 0
            for i in range(len(input)):
                cur_diff = calculate_diff(i, 0, input, diff)
                # print(f"Diff ({i}, {0}) = {cur_diff}")
                    
                if cur_diff != 0:
                    continue
                elif cur_diff == 0:
                    right_diff = calculate_diff(i, 1, input, diff)
                    if right_diff != 0:
                        continue
                    else:
                        # print(f"Diff {i}, {0} and its right is 0")
                        # print(f"On level {i}, diff becomes 0")
                        max_level = i                   
                        break

            for i in range(max_level, -1, -1):
                for j in range(len(input) - i):
                    # print(f"Update Diff {i}, {j}")
                    if i == max_level:
                        diff[i][j] = 0
                    elif j != 0:
                        diff[i][j] = diff[i][j-1] + diff[i+1][j-1]
                    # print(diff)

            next_num = input[-1] + diff[0][len(input)-1]
            # print(f"Next number of current line is {next_num}")

            res.append(next_num)

        total_sum = sum(res)
        print(f"Total sum is {total_sum}")


if __name__ == "__main__":
    main()