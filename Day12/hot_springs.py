#!/usr/bin/env python3 -u

import sys
from functools import cache

@cache
def calculate_arrangement(note: str, group: tuple[int]) -> int:
    if not note:
        return len(group) == 0

    if not group:
        return "#" not in note
    
    char, rest_of_note = note[0], note[1:]

    if char == ".":
        return calculate_arrangement(rest_of_note, group)

    if char == "#":
        cur_group = group[0]
        if (
            len(note) >= cur_group
            and all(c != "." for c in note[:cur_group])
            and (len(note) == cur_group or note[cur_group] != "#")
        ):
            return calculate_arrangement(note[cur_group + 1 :], group[1:])

        return 0
    
    if char == "?":
        return calculate_arrangement(f"#{rest_of_note}", group) + calculate_arrangement(f".{rest_of_note}", group)



def part_1(notes: list(), groups: list()) -> int:
    total_arr = 0

    for i in range(len(notes)):
        num_arr = calculate_arrangement(notes[i], groups[i])
        # print(f"{i}: {num_arr}")
        total_arr += num_arr

    return total_arr


def part_2(notes: list(), groups: list()) -> int:
    new_notes = list()
    new_groups = list()

    for note in notes:
        new_notes.append('?'.join([note for _ in range(5)]))

    for group in groups:
        new_groups.append(group * 5)

    total_arr = 0
    for i in range(len(notes)):
        num_arr = calculate_arrangement(new_notes[i], new_groups[i])
        # print(f"{i}: {num_arr}")
        total_arr += num_arr

    return total_arr
    

def main():
    filename = sys.argv[1]

    notes = list()
    groups = list()
    with open(filename, 'r') as file:
        for line in file:
            notes.append(line.split()[0])
            groups.append(tuple(map(int, line.split()[1].split(','))))

    # print(notes)
    # print(groups)

    part_1_res = part_1(notes, groups)

    part_2_res = part_2(notes, groups)

    print(f"{part_1_res}, {part_2_res}")


if __name__ == "__main__":
    main()