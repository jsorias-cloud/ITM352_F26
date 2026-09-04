#This program prompts the user to enter a temperature in Fahrenheit and then converts it to Celsius.
# Name: Jorryn Orias
# Date: Sept 4, 2026

Fahrenheit_input = input("Enter temperature in Fahrenheit: ")
Fahrenheit_float = float(Fahrenheit_input)

celsisus_value = (Fahrenheit_float - 32) * 5 / 9

celsisus_value = round(celsisus_value, 2)

print("You entered:", Fahrenheit_float)
print("The temperature in Celsius is:", celsisus_value)

