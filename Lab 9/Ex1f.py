# Open names.txt and read its contents
# Append a new name at the end of the file

with open("names.txt", "r") as file_object:
    contents_list = file_object.readlines()
    print(contents_list)

with open("names.txt", "a") as file_object:
    print("Appending a new name to the file...")
    file_object.write("Doe, John\n")
    
 #need the n in order to add a new line after the name so that it doesn't get added to the end of the last name in the file

# make sure to have intention and explain this intention in python! 


