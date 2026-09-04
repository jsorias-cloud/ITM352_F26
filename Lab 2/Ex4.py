# Ask the user to enter a decimal number. Calculate its square of that number and print it out.
# Name: Jorryn Orias
# Date: Sept 2, 2026

input_value = input("Enter a floating point number: ")
float_value = float(input_value)
squared_value = float_value ** 2
rounded_value = round(squared_value, 2)

print("you entered:", float_value)
print("The square of your number you entered is:", rounded_value,) 