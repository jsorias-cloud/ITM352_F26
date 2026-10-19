# Function for multiplying numbers
def multiply(x, y):
    result = x * y
    return result
 #was not returning anything, so the result was not being printed  
a = 5
b = 6
#int cannot be in quotation marks or it will be considered a string
#the values put into the function need to be a & b or there will be no value
result = multiply(a,b)
print(result)
