# Open a file and read its content 

with open("names.txt","r") as file_object:
    content = file_object.read()
    print(content)
    content_list = content.split("\n")
    #split can be used to split a string by a specified character and return a list of the resulting substrings
    print(f"Number of names: {len(content_list)} ")
    for name in content_list:
        print(name)
