# Read a file of names one line at a time and print each name

with open("names.txt","r") as file_object:
    while (line := file_object.readline()):
        print(line.strip())

        # a while loop contiunues to execute until it deems true?
        # strip removes whitespace frmo both ends of the line so that it doesn't...
        # print a blank line after each name
        # read --> read all the data in the file all at once 
        # readline --> reads one line at a time
        
