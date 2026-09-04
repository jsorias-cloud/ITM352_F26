# This program prompts the user to enter a temperature in Fahrenheit and then converts it to Celsius.
# Create the conversion as function.
# Name: Jorryn Orias
# Date: Sept 4, 2026

def F_to_C(Fahrenheit):
    celsisus = (Fahrenheit - 32) * 5 / 9
    rounded_celsius = round(celsisus, 2)
    return rounded_celsius


Fahrenheit_input = input("Enter a temperature in Fahrenheit: ")
Fahrenheit_float = float(Fahrenheit_input)

celsisus_value = F_to_C(Fahrenheit_float)

print("You entered:", Fahrenheit_float)
print("The temperature in Celsius is:", celsisus_value)

