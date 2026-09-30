# Write Python code that creates a list with a variety of different values. 
# Include control logic (if, elif, else) that will print different messages whether the list contains fewer than 5 elements, between 5 and 10 (inclusive), and more than 10 elements. 
# Test your code on lists with several different lengths.

def checkList_Length(my_list):

if len(my_list) < 5:
    print(f"List has {len(my_list)} elements: Fewer than 5 elements.")

elif 5 <= len(my_list) <= 10:
    print(f"List has {len(my_list)} elements: Between 5 and 10 elements (inclusive).")

else:
    print(f"List has {len(my_list)} elements: More than 10 elements.")

test_cases = [
    [1, 2],                                    # fewer than 5
    [1, 2, 3, 4],                               # fewer than 5
    [1, 2, 3, 4, 5],                            # exactly 5 (edge case)
    [1, 2, 3, 4, 5, 6, 7],                      # between 5 and 10
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],            # exactly 10 (edge case)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]         # more than 10
]

for case in test_cases:
    if len(case) < 5:
        print(f"{case} -> fewer than 5 elements")
    elif 5 <= len(case) <= 10:
        print(f"{case} -> between 5 and 10 elements")
    else:
        print(f"{case} -> more than 10 elements")


        
