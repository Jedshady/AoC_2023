#!/usr/bin/env python3 -u

import sys
import math
import copy

import logging

logging.basicConfig(level=logging.INFO, filemode='w')


def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

def on_segment(p, q, r):
    if min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]):
        return True
    return False

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, q1, p2): return True
    if o2 == 0 and on_segment(p1, q1, q2): return True
    if o3 == 0 and on_segment(p2, q2, p1): return True
    if o4 == 0 and on_segment(p2, q2, q1): return True

    return False



def main():
    filename = sys.argv[1]

    min_x = min_y = min_z_start = math.inf
    max_x = max_y = max_z_start = - math.inf

    initial_state = dict()
    z_to_bricks = dict()

    with open(filename, 'r') as file:
        for index, line in enumerate(file):         
            s_x, s_y, s_z = map(int, line.strip().split('~')[0].split(','))
            e_x, e_y, e_z = map(int, line.strip().split('~')[1].split(','))

            min_x = min(min_x, s_x, e_x)
            max_x = max(max_x, s_x, e_x)
            min_y = min(min_y, s_y, e_y)
            max_y = max(max_y, s_y, e_y)
            min_z_start = min(min_z_start, s_z)
            max_z_start = max(max_z_start, s_z)

            initial_state[index] = {'s_x': s_x, 's_y': s_y, 's_z': s_z, 'e_x': e_x, 'e_y': e_y, 'e_z': e_z}

            for h in range(s_z, e_z+1):
                if h in z_to_bricks:
                    z_to_bricks[h].append(index)
                else:
                    z_to_bricks[h] = []
                    z_to_bricks[h].append(index)


    # logging.critical(f"{initial_state=}")
    # logging.critical(f"{z_to_bricks=}")
    # logging.critical(f"{min_x=} {max_x=}\n{min_y=} {max_y=}\n{min_z_start=} {max_z_start=}")


    updated_state = copy.deepcopy(initial_state)
    updated_z_to_bricks = dict()
    
    supporting_state = dict()
    for idx in initial_state.keys():
        supporting_state[idx] = {'supported_by': [], 'supporting': []}

    for cur_z in range(min_z_start, max_z_start+1):
    # for cur_z in range(min_z_start, min_z_start+2):   # For testing purpose
        queue = []
        
        if cur_z in z_to_bricks:
            for brick_index in z_to_bricks[cur_z]:
                brick_loc = initial_state[brick_index]

                # Only add bricks that have start point on current height cur_z to the queue
                if brick_loc['s_z'] == cur_z:
                    queue.append((brick_index, brick_loc))
        

        logging.debug(f"{cur_z=} {queue=}")
        while queue:
            b_idx, b_loc = queue.pop()
            final_z = b_loc['s_z']
            b_height = b_loc['e_z'] - b_loc['s_z']

            b_start, b_end =  (b_loc['s_x'], b_loc['s_y']), (b_loc['e_x'], b_loc['e_y'])

            logging.debug(f"{b_loc=}")

            # Test every z below
            for test_z in range(cur_z - 1, 0, -1):
                logging.debug(f"{test_z=}")
                if test_z in updated_z_to_bricks:
                    intersect_with_any = False
                    # there are bricks on this test level, need to see if they intersect
                    for test_b_idx in updated_z_to_bricks[test_z]:
                        test_b_loc = updated_state[test_b_idx]
                        logging.debug(f"{test_b_loc=}")
                        
                        test_b_start, test_b_end = (test_b_loc['s_x'], test_b_loc['s_y']), (test_b_loc['e_x'], test_b_loc['e_y'])

                        logging.debug(f"{b_start=} {b_end=} {test_b_start=} {test_b_end}")
                        is_intersect = do_intersect(b_start, b_end, test_b_start, test_b_end)
                        logging.debug(f"{is_intersect=}")

                        if is_intersect:
                            intersect_with_any = True
                            supporting_state[b_idx]['supported_by'].append(test_b_idx)
                            supporting_state[test_b_idx]['supporting'].append(b_idx)

                    if intersect_with_any:
                        break
                    else:
                        final_z = test_z

                else:
                    # there is no brick on this test level, good to go down
                    final_z = test_z
            
            logging.debug(f"{final_z=}")
            
            b_loc['s_z'] = final_z
            b_loc['e_z'] = final_z + b_height

            updated_state[b_idx] = b_loc

            for z in range(final_z, final_z + b_height + 1):
                if z in updated_z_to_bricks:
                    updated_z_to_bricks[z].append(b_idx)
                else:
                    updated_z_to_bricks[z] = []
                    updated_z_to_bricks[z].append(b_idx)

            # logging.debug(f"{updated_state=}")
            logging.debug(f"{updated_z_to_bricks=}")
            # logging.debug(f"{supporting_state=}") 
            logging.debug(f"*********************************")    

    logging.debug(f"{updated_z_to_bricks=}")
    logging.debug(f"{supporting_state=}") 
    
    
    bricks_to_fall = dict()

    for key in supporting_state.keys():
        bricks_to_fall[key] = set()

    for b_idx, s_state in supporting_state.items():
        if s_state['supporting']:
            # Default: will_cause_collapse = False

            to_collapse_queue = []
            for test_b_idx in s_state['supporting']:
                if len(supporting_state[test_b_idx]['supported_by']) < 2:
                    # will_cause_collapse = True
                    to_collapse_queue.append(test_b_idx)
                    bricks_to_fall[b_idx].add(test_b_idx)

            while to_collapse_queue:
                cur_collapse = to_collapse_queue.pop()
                bricks_cur_collapse_supporting = supporting_state[cur_collapse]['supporting'] 

                if bricks_cur_collapse_supporting:
                    for test_b_idx in bricks_cur_collapse_supporting:
                        # Default: current test_b_idx is not supported
                        will_be_supported = False
                        bricks_supporting_test_b_idx = supporting_state[test_b_idx]['supported_by'] 
                        for supporting_brick in bricks_supporting_test_b_idx:
                            if supporting_brick not in bricks_to_fall[b_idx]:
                                # Found a supporting brick that supports test_b_idx so that it does not fall
                                # test_b_idx will be supported
                                will_be_supported = True
                        
                        if not will_be_supported:
                            to_collapse_queue.append(test_b_idx)
                            bricks_to_fall[b_idx].add(test_b_idx)


    total_num = 0
    for b_idx, b_to_fall in bricks_to_fall.items():
        logging.debug(f"{b_idx=} {b_to_fall=}")
        total_num += len(b_to_fall)

    print(total_num)           


if __name__ == "__main__":
    main()