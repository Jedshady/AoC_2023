def modify_list(lst):
    lst.append(4)
    print("Inside function:", lst)

# Original list
original_list = [1, 2, 3]

# Pass a copy
modify_list(original_list[:])  # Using slicing
# or
# modify_list(list(original_list))  # Using list constructor

print("Outside function:", original_list)