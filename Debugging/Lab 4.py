# Retrieving elements from a list
def get_element(list, index):
    return list[index - 1]

#the index started from 0, so it needs to be subtracted by 1 to get the right value

my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
print(get_element(my_list, 5))

