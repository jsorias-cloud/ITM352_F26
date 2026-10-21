# Open a file using "with"
# All the text that follows the with statement is in the scope of the file being open 
# don't have to say close because it is built into the with statement

with open("names.txt","r") as file_object:
    print(type(file_object))

print("The file is now closed:", file_object.closed)

