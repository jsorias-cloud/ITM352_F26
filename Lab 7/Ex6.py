#6a in Lab 
data = ("hello", "10", "goodbye", 3, "goodnight", 5)

value=input("Enter a value to append to the tuple: ")

data.append(value)

print(data)

#6c in Lab
data = ("hello", "10", "goodbye", 3, "goodnight", 5)

value=input("Enter a value to append to the tuple: ")

data.append(value)

print(f"Attempted to append {value!r} to the tuple. Error: {error}")

#6d in Lab

# Create a new tuple by concatenating the input as a one-item tuple.

data = ("hello", "10", "goodbye", 3, "goodnight", 5)

value=input("Enter a value to append to the tuple: ")

data.append(value)

concatenated_data = data + (value,)
print("Appended with +:", concatenated_data)


#6e in Lab
# The unpacking operator creates a new tuple with the input at the end.

data = ("hello", "10", "goodbye", 3, "goodnight", 5)

value=input("Enter a value to append to the tuple: ")

data.append(value)

unpacked_data = (*data, value)
print("Appended with *:", unpacked_data)


#6f in Lab

data = ("hello", "10", "goodbye", 3, "goodnight", 5)

value=input("Enter a value to append to the tuple: ")

data.append(value)

list_data = list(data)
list_data.append(value)
appended_data = tuple(list_data)
print("Appended with list.append():", appended_data)
